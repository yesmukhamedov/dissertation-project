"""Announce every table that breaks across a page with a "Continuation of table N" line.

GOST 7.32 requires it — the label, number and title are given once, above the
first part; over each further part the word "Continuation" and the number are
repeated on the left. Ten of the sixteen dissertations published by this council
carry the line (`council/en/10-dissertation/peer-norms.md` section 8); a table
that breaks without one is a formal defect, and the assembled volume had 42
tables and not a single continuation.

Pagination is not knowable to python-docx, so this runs as a post-pass on the
saved .docx under Word COM: for each table it finds the first row that starts on
a later page than the table does, duplicates the head row there, splits the table
at that point, and writes the continuation line into the paragraph the split
leaves behind.

Three rules keep the line where GOST wants it — at the head of a page, once:

* The split is nailed down with a hard page break on the continuation line, so
  the label cannot drift into the middle or the foot of a page when a later edit
  changes how much fits above it. Measuring alone is not enough: a split is
  committed the moment it is made, and the header row it inserts moves every
  break after it.
* Tables are walked front to back. Splitting adds a paragraph and a row, which
  pushes the rest of the document down; a table's own split therefore has to be
  fixed before anything ahead of it moves.
* A table whose first part would be nothing but its head row is not split at all
  — the whole table is pushed to the next page instead, caption and all. That is
  what a caption plus a bare ribbon of column heads at the foot of page 86 (KZ
  table 3.14, 2026-08-23 build) should have been.

The head row is duplicated *inside* the table before the split, so Word builds it
against the table's own column grid. Pasting a row across from the other half of
the split instead — which is what the first version of this pass did — carries
the source column widths with it and leaves the continued part with a grid of 11
columns under a 6-column head.

The pass is idempotent: a table whose preceding paragraph is already a
continuation line is left alone, so building twice does not stack lines.

Usage:
    import table_continuations
    table_continuations.apply(word, docx_path, lang="en")
"""
from __future__ import annotations

import re
import time
from pathlib import Path

# wdActiveEndPageNumber — the page a range ends on, counted from the document start.
_WD_ACTIVE_END_PAGE = 3


def _safe(fn):
    """Retry a COM call through transient RPC_E_CALL_REJECTED ("call was rejected
    by callee") when Word is momentarily busy with its own layout pass. This pass
    calls Information()/Repaginate() far more often than `build_toc.dump_pages`
    does (once per split, per table, per document), so the same retry `build_toc`
    already relies on is needed here too — see its `_safe`.
    """
    for _ in range(10):
        try:
            return fn()
        except Exception:
            time.sleep(0.4)
    return fn()


# A rendered table caption, as `md2gost._table_caption` normalises it:
# "Table 4.4 – Title" in English, "Кесте 4.4 – Атауы" in Kazakh.
_CAPTION = re.compile(r"^\s*(?:Table|Кесте|Таблица)\s+([\w.]+)\s*[–—-]", re.IGNORECASE)

_CONTINUATION = {
    "en": "Continuation of table {num}",
    # Kazakh hyphenates a numeral bound to the noun it counts. The council's one
    # Kazakh-language precedent writes it that way ("1.1-кестенің жалғасы",
    # Toktarova, pp. 16/35/43/108), and so does this manuscript's own prose —
    # 59 references of the form "Б.1-кесте", "2.3-кестеде" against a single
    # spaced one. The spaced form contradicted both.
    "kz": "{num}-кестенің жалғасы",
    "ru": "Продолжение таблицы {num}",
}

# Recognises a line this pass wrote on an earlier run, in any of the three forms.
_ALREADY = re.compile(
    r"^\s*(?:Continuation\s+of\s+table|Продолжение\s+таблицы)\b|кестенің\s+жалғасы\s*$",
    re.IGNORECASE,
)

# A table split more times than this is a runaway, not a long table; the guard
# keeps a measurement bug from appending lines until Word runs out of memory.
_MAX_SPLITS_PER_TABLE = 40

# Smallest first part worth leaving behind: the head row plus one row of data.
# A break above this is not a break, it is a stranded caption — the table goes to
# the next page whole instead.
_MIN_FIRST_PART_ROWS = 2


def _page_of(doc, pos: int) -> int:
    """1-based page number of a character position."""
    return int(_safe(lambda: doc.Range(pos, pos).Information(_WD_ACTIVE_END_PAGE)))


def _caption_index(doc, table) -> int | None:
    """Index, within the text before `table`, of its caption paragraph — or None.

    Looks back over at most a few paragraphs: the caption sits directly above its
    table, but a split can leave an empty paragraph in between. An index is
    returned rather than the Paragraph itself because a Paragraph drawn from a
    temporary Range dies with that Range: caching one and setting a format on it
    a few statements later raises E_OUTOFMEMORY. Callers re-resolve it against a
    Range they hold open — see `_caption_of`.
    """
    rng = doc.Range(0, table.Range.Start)
    n = rng.Paragraphs.Count
    for back in range(0, min(4, n)):
        text = rng.Paragraphs(n - back).Range.Text.strip()
        if not text:
            continue
        return n - back if _CAPTION.match(text) else None
    return None


def _caption_of(doc, table) -> tuple[str, str] | tuple[None, None]:
    """`(caption text, table number)` for `table`, or `(None, None)` if unlabelled."""
    rng = doc.Range(0, table.Range.Start)
    idx = _caption_index(doc, table)
    if idx is None:
        return (None, None)
    text = rng.Paragraphs(idx).Range.Text.strip()
    return (text, _CAPTION.match(text).group(1))


def _push_to_next_page(doc, table) -> bool:
    """Start `table` on a fresh page by breaking before its caption. True on success."""
    rng = doc.Range(0, table.Range.Start)   # held open while the format is set
    idx = _caption_index(doc, table)
    if idx is None:
        return False
    rng.Paragraphs(idx).Range.ParagraphFormat.PageBreakBefore = True
    return True


def _preceded_by_continuation(doc, table) -> bool:
    rng = doc.Range(0, table.Range.Start)
    n = rng.Paragraphs.Count
    for back in range(0, min(3, n)):
        text = rng.Paragraphs(n - back).Range.Text.strip()
        if not text:
            continue
        return bool(_ALREADY.search(text))
    return False


def _copy_cell(src_cell, dst_cell) -> None:
    """Copy one cell's content, with its run formatting, into another cell.

    Both ranges are shortened by one character first: a cell's range ends on the
    end-of-cell marker, and assigning FormattedText that carries that marker adds
    a cell rather than filling one.
    """
    try:
        s, d = src_cell.Range, dst_cell.Range
        s.End = s.End - 1
        d.End = d.End - 1
        d.FormattedText = s.FormattedText
    except Exception:
        try:
            dst_cell.Range.Text = src_cell.Range.Text.rstrip("\r\x07")
            dst_cell.Range.Bold = True
        except Exception:
            pass


def _insert_header_copy(table, at_index: int) -> bool:
    """Duplicate `table`'s head row immediately above row `at_index`. True on success.

    Done before the split, inside the table, so the copy is laid out on the
    table's own column grid; see the module docstring on why a row pasted across
    from the other half arrives with the wrong grid.
    """
    try:
        src = table.Rows(1)
        table.Rows.Add(BeforeRow=table.Rows(at_index))
        dst = table.Rows(at_index)
    except Exception:
        return False
    for i in range(1, min(src.Cells.Count, dst.Cells.Count) + 1):
        _copy_cell(src.Cells(i), dst.Cells(i))
    try:
        dst.AllowBreakAcrossPages = False
    except Exception:
        pass
    return True


def _split_at(doc, table, row_index: int, label: str):
    """Split `table` before `row_index`; write `label` in the gap; return the new table.

    `row_index` must already be the duplicated head row, so the new table opens
    on its own heading.
    """
    new_table = table.Split(row_index)
    # Word leaves exactly one empty paragraph between the two parts. Writing to
    # the paragraph's whole range would replace its paragraph MARK as well, which
    # joins the two tables straight back into one — the text then vanishes and the
    # split is undone. Write to the range that stops one character short of the
    # mark instead.
    gap = doc.Range(table.Range.End, new_table.Range.Start).Paragraphs(1)
    doc.Range(gap.Range.Start, gap.Range.End - 1).Text = label
    gap = doc.Range(table.Range.End, new_table.Range.Start).Paragraphs(1)
    gap.Range.Bold = False
    gap.Range.Italic = False
    fmt = gap.Range.ParagraphFormat
    fmt.Alignment = 0          # wdAlignParagraphLeft
    fmt.FirstLineIndent = 0
    fmt.SpaceBefore = 0
    fmt.SpaceAfter = 0
    fmt.KeepWithNext = True
    # The break is what pins the label to the head of the page; see the module
    # docstring. Without it the label sits wherever the last measurement left it.
    fmt.PageBreakBefore = True
    try:
        new_table.Rows(1).HeadingFormat = True
    except Exception:
        pass
    return new_table


def _first_row_on_later_page(doc, table, first_page: int) -> int | None:
    """Index of the first row that starts on a page after `first_page`."""
    return next(
        (r for r in range(2, table.Rows.Count + 1)
         if _page_of(doc, table.Rows(r).Range.Start) > first_page),
        None,
    )


def apply(word, docx_path: Path, lang: str = "en") -> int:
    """Add continuation lines to every split table in `docx_path`. Returns the count.

    `word` is a live Word.Application COM object, as `build_full_dissertation`
    already holds one. The document is opened, edited in place and saved.
    """
    template = _CONTINUATION.get(lang, _CONTINUATION["en"])
    doc = _safe(lambda: word.Documents.Open(str(Path(docx_path).resolve())))
    added = 0
    try:
        _safe(doc.Repaginate)
        # Front to back, over table objects captured up front: Word keeps a Table
        # reference valid and auto-shifted as the surrounding document is edited,
        # so `Tables.Count` growing under us as tables split does not matter.
        for table in [doc.Tables(i) for i in range(1, doc.Tables.Count + 1)]:
            if _preceded_by_continuation(doc, table):
                continue
            _, num = _caption_of(doc, table)
            if num is None:
                continue  # an unlabelled layout table, not a numbered one
            label = template.format(num=num)
            pushed = False
            for _ in range(_MAX_SPLITS_PER_TABLE):
                first_page = _page_of(doc, table.Range.Start)
                if _page_of(doc, table.Range.End) == first_page:
                    break
                cut = _first_row_on_later_page(doc, table, first_page)
                if cut is None:
                    break  # spills over but no row starts later: nothing to announce
                # A single data row left behind on the continued part reads as a
                # stray; carry one more row over when the first part can spare it.
                if table.Rows.Count - cut == 0 and cut - 1 > _MIN_FIRST_PART_ROWS:
                    cut -= 1
                if cut - 1 < _MIN_FIRST_PART_ROWS:
                    # Only the head row fits above the break. Move the whole table,
                    # caption included, onto the next page and measure again.
                    if pushed or not _push_to_next_page(doc, table):
                        break
                    pushed = True
                    _safe(doc.Repaginate)
                    continue
                if not _insert_header_copy(table, cut):
                    break
                table = _split_at(doc, table, cut, label)
                added += 1
                _safe(doc.Repaginate)
        _safe(doc.Save)
    finally:
        _safe(lambda: doc.Close(SaveChanges=0))
    return added
