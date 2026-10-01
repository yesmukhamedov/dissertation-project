"""Append review tasks to a round file: python work/addtask.py <round.json> < tasks(JSON list of [chapter_dir, file_id, chunk, [issues]])"""
import json, sys, os
p = sys.argv[1]
cur = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
for ch, f, n, iss in json.loads(sys.stdin.buffer.read().decode("utf-8")):
    cur.append({"out": f"chapters/{ch}/translated-kk-qwen/{f}-kz.md", "chunk": n, "issues": iss})
json.dump(cur, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(cur), "tasks in", p)
