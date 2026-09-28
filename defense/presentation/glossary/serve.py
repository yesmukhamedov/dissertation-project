"""Glossary server: serves index.html and keeps terms.csv / usage.csv with a change log.

Run:  python serve.py [--port 8765]   then open http://localhost:8765

Files (UTF-8 with BOM, ';' separated — open in Excel as is):
    terms.csv    one row per term: id;kk;ru;en;kind;note;status;updated
    usage.csv    where a term is used: id;author;slug;year;lang;slide;rubric;quote;source
    history.csv  append-only log: ts;table;id;action;field;old;new;comment
    usage.md     readable "term -> who uses it on which slide", rebuilt after every change

Edits made outside the page (Excel, text editor) are detected on the next request by
comparing with the snapshot in .snapshot/ and logged with comment "вне страницы".
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

HERE = Path(__file__).resolve().parent
SNAP = HERE / ".snapshot"
TABLES = {
    "terms": ["id", "kk", "ru", "en", "kind", "note", "status", "updated"],
    "usage": ["id", "author", "slug", "year", "lang", "slide", "rubric", "quote", "source"],
}
KEYS = {"terms": ("id",), "usage": ("id", "slug", "slide", "lang", "quote")}
HISTORY = ["ts", "table", "id", "action", "field", "old", "new", "comment"]
LOCK = Lock()


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_csv(path: Path, cols: list[str]) -> list[dict[str, str]]:
    """Read a ';' CSV; missing file -> empty list, missing columns -> ''."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [{c: (r.get(c) or "") for c in cols} for r in csv.DictReader(f, delimiter=";")]


def write_csv(path: Path, cols: list[str], rows: list[dict[str, str]]) -> None:
    """Write atomically so Excel or a crash never sees a half-written file."""
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(path)


def log(entries: list[dict[str, str]]) -> None:
    path = HERE / "history.csv"
    new = not path.exists()
    with path.open("a", encoding="utf-8-sig" if new else "utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HISTORY, delimiter=";")
        if new:
            w.writeheader()
        w.writerows(entries)


def key(table: str, row: dict[str, str]) -> str:
    return " | ".join(row[k] for k in KEYS[table])


def diff(table: str, old: list[dict], new: list[dict], comment: str) -> list[dict[str, str]]:
    """Field-level differences between two versions of a table, as history rows."""
    ts, cols = now(), TABLES[table]
    a = {key(table, r): r for r in old}
    b = {key(table, r): r for r in new}
    out = []
    for k in b.keys() - a.keys():
        out.append(dict(ts=ts, table=table, id=k, action="create", field="", old="",
                        new=json.dumps(b[k], ensure_ascii=False), comment=comment))
    for k in a.keys() - b.keys():
        out.append(dict(ts=ts, table=table, id=k, action="delete", field="",
                        old=json.dumps(a[k], ensure_ascii=False), new="", comment=comment))
    for k in a.keys() & b.keys():
        for c in cols:
            if c != "updated" and a[k][c] != b[k][c]:
                out.append(dict(ts=ts, table=table, id=k, action="update", field=c,
                                old=a[k][c], new=b[k][c], comment=comment))
    return out


def sync_external() -> None:
    """Log edits made to the CSV files outside the page since the last snapshot."""
    SNAP.mkdir(exist_ok=True)
    for t, cols in TABLES.items():
        cur_path, snap_path = HERE / f"{t}.csv", SNAP / f"{t}.csv"
        if not snap_path.exists():
            if cur_path.exists():
                shutil.copyfile(cur_path, snap_path)
            continue
        cur, snap = read_csv(cur_path, cols), read_csv(snap_path, cols)
        if cur != snap:
            log(diff(t, snap, cur, "вне страницы"))
            shutil.copyfile(cur_path, snap_path)


def save(table: str, rows: list[dict[str, str]], comment: str) -> int:
    cols = TABLES[table]
    path = HERE / f"{table}.csv"
    old = read_csv(path, cols)
    rows = [{c: str(r.get(c, "")).strip() for c in cols} for r in rows]
    entries = diff(table, old, rows, comment)
    if not entries:
        return 0
    if table == "terms":
        touched = {e["id"] for e in entries}
        for r in rows:
            if r["id"] in touched:
                r["updated"] = now()[:10]
    write_csv(path, cols, rows)
    shutil.copyfile(path, SNAP / f"{table}.csv")
    log(entries)
    build_usage_md()
    return len(entries)


def build_usage_md() -> None:
    """usage.md: for every term — its three forms and who uses it on which slide."""
    terms = read_csv(HERE / "terms.csv", TABLES["terms"])
    usage = read_csv(HERE / "usage.csv", TABLES["usage"])
    by_id: dict[str, list[dict]] = {}
    for u in usage:
        by_id.setdefault(u["id"], []).append(u)
    lines = ["# Словарь: где используется каждый термин", "",
             f"Собрано из terms.csv и usage.csv {now()}. Не править руками — файл пересобирается.", ""]
    for t in sorted(terms, key=lambda r: r["id"]):
        lines.append(f"## {t['id']}")
        lines.append(f"- kk: {t['kk'] or '—'}")
        lines.append(f"- ru: {t['ru'] or '—'}")
        lines.append(f"- en: {t['en'] or '—'}")
        if t["note"]:
            lines.append(f"- примечание: {t['note']}")
        us = sorted(by_id.get(t["id"], []), key=lambda u: (u["slug"] != "A17", -int(u["year"] or 0), u["slug"]))
        if us:
            lines.append("")
            lines.append("| Кто | Год | Слайд | Яз. | Цитата |")
            lines.append("|---|---|---|---|---|")
            for u in us:
                q = u["quote"].replace("|", "/")
                where = u["slide"] if u["slide"] == u["rubric"] else f"{u['slide']} {u['rubric']}"
                lines.append(f"| {u['author'] or u['slug']} | {u['year']} | {where} | {u['lang']} | {q} |")
        lines.append("")
    (HERE / "usage.md").write_text("\n".join(lines), encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj: object, code: int = 200) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            self._send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/data":
            with LOCK:
                sync_external()
                self._json({t: read_csv(HERE / f"{t}.csv", c) for t, c in TABLES.items()}
                           | {"history": read_csv(HERE / "history.csv", HISTORY)})
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/save":
            return self._send(404, b"not found", "text/plain")
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
        table = body.get("table")
        if table not in TABLES:
            return self._json({"error": "unknown table"}, 400)
        with LOCK:
            sync_external()
            n = save(table, body.get("rows", []), body.get("comment", "").strip() or "страница")
        self._json({"changes": n})

    def log_message(self, *_: object) -> None:
        pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    for t, cols in TABLES.items():
        if not (HERE / f"{t}.csv").exists():
            write_csv(HERE / f"{t}.csv", cols, [])
    sync_external()
    build_usage_md()
    url = f"http://localhost:{a.port}"
    print(f"Словарь: {url}  (Ctrl+C — остановить)")
    if not a.no_browser:
        webbrowser.open(url)
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
