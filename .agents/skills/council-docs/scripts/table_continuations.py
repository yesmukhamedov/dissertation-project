"""Announce every table that breaks across a page with a "Continuation of table N" line.

GOST 7.32 requires it — the label, number and title are given once, above the
first part; over each further part the word "Continuation" and the number are
repeated on the left. Ten of the sixteen dissertations published by this council
carry the line (`council/en/10-dissertation/peer-norms.md` section 8); a table
that breaks without one is a formal defect, and the assembled volume had 42
tables and not a single continuation.

Pagination is not knowable to python-docx, so this runs as a post-pass on the
saved .docx under Word COM: for each table it finds the first row that starts on
a later page than the table does, splits the table there, writes the continuation
line into the paragraph the split leaves behind, and repeats the header row over
the continued part. `md2gost._repeat_header_row` has already marked row 1 as a
header, which is what makes the *first* break repeat its head; after a split the
new table needs its own copy, which is added here.

The pass is idempotent: a table whose preceding paragraph is already a
continuation line is left alone, so building twice does not stack lines.

Usage:
    import table_continuations
    table_continuations.apply(word, docx_path, lang="en")
"""
from __future__ import annotations

import re
from pathlib import Path

# wdActiveEndPageNumber — the page a range ends on, counted from the document start.
_WD_ACTIVE_END_PAGE = 3

# A rendered table caption, as `md2gost._table_caption` normalises it:
# "Table 4.4 – Title" in English, "Кесте 4.4 – Атауы" in Kazakh.
_CAPTION = re.compile(r"^\s*(?:Table|Кесте|Таблица)\s+([\w.]+)\s*[–—-]", re.IGNORECASE)

_CONTINUATION = {
    "en": "Continuation of table {num}",
    "kz": "{num} кестенің жалғасы",
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


def _page_of(doc, pos: int) -> int:
    """1-based page number of a character position."""
    return int(doc.Range(pos, pos).Information(_WD_ACTIVE_END_PAGE))


def _caption_number(doc, table) -> str | None:
    """Number from the caption above `table`, e.g. "4.4", or None if unlabelled.

    Looks back over at most a few paragraphs: the caption sits directly above its
    table, but a split can leave an empty paragraph in between.
    """
    rng = doc.Range(0, table.Range.Start)
    n = rng.Paragraphs.Count
    for back in range(0, min(4, n)):
        text = rng.Paragraphs(n - back).Range.Text.strip()
        if not text:
            continue
        m = _CAPTION.match(text)
        return m.group(1) if m else None
    return None


def _preceded_by_continuation(doc, table) -> bool:
    rng = doc.Range(0, table.Range.Start)
    n = rng.Paragraphs.Count
    for back in range(0, min(3, n)):
        text = rng.Paragraphs(n - back).Range.Text.strip()
        if not text:
            continue
        return bool(_ALREADY.search(text))
    return False


def _copy_header_row(src_table, dst_table) -> None:
    """Put a copy of `src_table`'s header row at the top of `dst_table`.

    Word's Table.Split does not carry the repeating header over to the new table,
    so the continued part would otherwise open on a data row. The row is copied as
    formatted text where Word allows it, and cell-by-cell as bold text where it
    does not.
    """
    dst_table.Rows.Add(BeforeRow=dst_table.Rows(1))
    new_row = dst_table.Rows(1)
    try:
        new_row.Range.FormattedText = src_table.Rows(1).Range.FormattedText
    except Exception:
        for i in range(1, src_table.Columns.Count + 1):
            try:
                text = src_table.Cell(1, i).Range.Text.rstrip("\r\x07")
                cell = new_row.Cells(i)
                cell.Range.Text = text
                cell.Range.Bold = True
            except Exception:
                pass
    new_row.HeadingFormat = True


def _split_at(doc, table, row_index: int, label: str):
    """Split `table` before `row_index`; write `label` in the gap; return the new table."""
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
    gap.Range.ParagraphFormat.Alignment = 0          # wdAlignParagraphLeft
    gap.Range.ParagraphFormat.FirstLineIndent = 0
    gap.Range.ParagraphFormat.SpaceBefore = 6
    gap.Range.ParagraphFormat.SpaceAfter = 0
    gap.Range.ParagraphFormat.KeepWithNext = True
    _copy_header_row(table, new_table)
    return new_table


def apply(word, docx_path: Path, lang: str = "en") -> int:
    """Add continuation lines to every split table in `docx_path`. Returns the count.

    `word` is a live Word.Application COM object, as `build_full_dissertation`
    already holds one. The document is opened, edited in place and saved.
    """
    template = _CONTINUATION.get(lang, _CONTINUATION["en"])
    doc = word.Documents.Open(str(Path(docx_path).resolve()))
    added = 0
    try:
        doc.Repaginate()
        # Back to front: splitting a table renumbers the ones after it, but never
        # the ones before, so walking backwards keeps every index valid.
        for idx in range(doc.Tables.Count, 0, -1):
            table = doc.Tables(idx)
            if _preceded_by_continuation(doc, table):
                continue
            num = _caption_number(doc, table)
            if num is None:
                continue  # an unlabelled layout table, not a numbered one
            label = template.format(num=num)
            for _ in range(_MAX_SPLITS_PER_TABLE):
                first_page = _page_of(doc, table.Range.Start)
                if _page_of(doc, table.Range.End) == first_page:
                    break
                # First row whose top falls on a later page than the table's.
                cut = next(
                    (r for r in range(2, table.Rows.Count + 1)
                     if _page_of(doc, table.Rows(r).Range.Start) > first_page),
                    None,
                )
                if cut is None:
                    break  # spills over but no row starts later: nothing to announce
                table = _split_at(doc, table, cut, label)
                added += 1
                doc.Repaginate()
        doc.Save()
    finally:
        doc.Close(SaveChanges=0)
    return added
