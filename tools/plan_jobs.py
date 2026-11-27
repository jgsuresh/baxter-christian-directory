"""Split a stretch of a source text into writer jobs of about 190 lines each.

Each job is one output file. Splits fall on paragraph boundaries, preferring a
paragraph that opens a new Direction, Objection, margin note, etc.

Usage (from the repository root):

    python3 tools/plan_jobs.py baxter-christian-directory part2 \
        --chapter 1 --end 5123 \
        --section 120 "Chapter 1 title and Directions 1-10" \
        --section 980 "Directions 11-20" \
        > jobs.json

--section gives the first source line and a short description of each
natural section (a Title, a Part, a run of Directions), in order; --end is the
last source line of the chapter. Find the lines with grep -n on the source.
The output is the job list the modernize workflow takes as args.jobs.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Lines that make a good place to start a new job (Baxter's labels; extend for other authors).
DEFAULT_HEADING = r"^\s*_?(Grand Direct|Direct|Tempt|Object|Quest|Tit|Sign|Rule|Motive|Answ)\b|^\s*\[Sidenote"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("work")
    ap.add_argument("volume")
    ap.add_argument("--chapter", required=True, help="chapter number or short label used in file names, e.g. 3")
    ap.add_argument("--chapter-name", default=None, help='how labels name the chapter, default "Chapter N"')
    ap.add_argument("--section", nargs=2, action="append", metavar=("START", "NAME"), required=True)
    ap.add_argument("--end", type=int, required=True, help="last source line (inclusive)")
    ap.add_argument("--target", type=int, default=190, help="target lines per job")
    args = ap.parse_args()

    work = json.load(open(os.path.join(ROOT, "works", args.work, "work.json"), encoding="utf-8"))
    vol = work["volumes"][args.volume]
    src = os.path.join(ROOT, "works", args.work, vol["source"])
    lines = open(src, encoding="utf-8").read().split("\n")
    heading = re.compile(work.get("heading_regex", DEFAULT_HEADING))
    L = lambda n: lines[n - 1]

    def para_start(n):
        return L(n - 1).strip() == "" and L(n).strip() != ""

    def best_cut(lo, hi, ideal):
        best, score = ideal, 10 ** 9
        for n in range(max(lo + 20, ideal - 45), min(hi - 20, ideal + 45) + 1):
            if para_start(n):
                d = abs(n - ideal) - (25 if heading.match(L(n)) else 0)
                if d < score:
                    best, score = n, d
        return best

    def context(n, lo):
        for k in range(n, lo - 1, -1):
            if re.match(r"^\s*_?(Grand Direct|Direct|Quest|Object|Tempt)\b", L(k)):
                return re.sub(r"\s+", " ", L(k).strip())[:150]
        return ""

    chap = str(args.chapter)
    tag = f"{int(chap):02d}" if chap.isdigit() else chap
    cname = args.chapter_name or (f"Chapter {chap}" if chap.isdigit() else chap)
    sections = [(int(a), b) for a, b in args.section]
    lo = sections[0][0]
    jobs = []
    for si, (a, name) in enumerate(sections):
        b = sections[si + 1][0] - 1 if si + 1 < len(sections) else args.end
        size = b - a + 1
        n = max(1, round(size / args.target))
        cuts = [a]
        for i in range(1, n):
            cuts.append(best_cut(cuts[-1], b, a + round(size * i / n)))
        cuts.append(b + 1)
        for p in range(n):
            s, e = cuts[p], cuts[p + 1] - 1
            jobs.append({
                "id": f"c{tag}s{si + 1}p{p + 1}",
                "start": s, "end": e,
                "prefix": f"ch{tag}-{si + 1:02d}-p{p + 1}-",
                "label": f"{cname}, section {si + 1} ({name})" + (f", part {p + 1} of {n}" if n > 1 else ""),
                "ctx": context(s, lo),
                "part": p + 1, "parts": n,
            })
    json.dump(jobs, sys.stdout, indent=1)
    print(f"\n{len(jobs)} jobs, {sum(j['end'] - j['start'] + 1 for j in jobs)} lines", file=sys.stderr)


if __name__ == "__main__":
    main()
