"""Mechanical checks on modernized files: run after every writing round.

Usage (from the repository root):

    python3 tools/check.py baxter-christian-directory part1            # whole volume
    python3 tools/check.py baxter-christian-directory part1 --prefix ch10-

Checks:
  coverage    source_lines of the files tile the source with no overlap; any
              gap that holds real text (not blank lines or footnote blocks) is listed
  duplicates  two files for the same range (an agent retry that left a copy)
  length      modernized body words / original words: outside 0.85-1.20 is a
              problem, outside 0.95-1.12 is listed as worth a look
  footnotes   every [n] marker in the source range is in the file, and its note
              is under the author's notes
  archaisms   thou/thee/thy/thine/hath/doth/saith/unto/whither left in the body
  headings    bold Direction headings run into their paragraph
Gaps listed under "known_gaps" in work.json (with the reason) are not reported.
Exit status is 1 if anything needs attention.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHAIC = re.compile(r"\b(thou|thee|thy|thine|hath|doth|saith|unto|whither|thither)\b", re.I)
# Fixed theological phrases kept on purpose (see GLOSSARY.md).
KEPT_PHRASES = re.compile(r"repentance unto life", re.I)


def body_of(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return re.split(r"^## (?:[^\n]*'s notes|Translator's notes)\s*$", text, maxsplit=1, flags=re.M)[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("work")
    ap.add_argument("volume")
    ap.add_argument("--prefix", default="", help="only check files whose names start with this")
    args = ap.parse_args()

    wdir = os.path.join(ROOT, "works", args.work)
    vol = json.load(open(os.path.join(wdir, "work.json"), encoding="utf-8"))["volumes"][args.volume]
    src = open(os.path.join(wdir, vol["source"]), encoding="utf-8").read().split("\n")
    files = sorted(glob.glob(os.path.join(wdir, vol["dir"], args.prefix + "*.md")))
    problems = []
    notes_only = []
    ranges = []

    for f in files:
        name = os.path.basename(f)
        text = open(f, encoding="utf-8").read()
        m = re.search(r"^source_lines: (\d+)-(\d+)", text, flags=re.M)
        if not m:
            problems.append(f"{name}: no source_lines in front matter")
            continue
        a, b = int(m.group(1)), int(m.group(2))
        ranges.append((a, b, name))
        orig = "\n".join(src[a - 1:b])
        # A footnote block inside the range (e.g. at a chapter's end) is compared with the notes, not the text.
        orig = re.split(r"^(?:FOOTNOTES:|\[\d+\] )", orig, maxsplit=1, flags=re.M)[0]
        body = body_of(text)
        notes = text[len(text) - len(text.split("## ", 1)[-1]):] if "## " in text else ""

        ow = len(re.sub(r"\[Sidenote:[^\]]*\]", " ", orig).split())
        bw = len(re.sub(r"^\*In the margin[^\n]*", " ", body, flags=re.M).split())
        if ow > 50 and not 0.85 <= bw / ow <= 1.20:
            problems.append(f"{name}: length ratio {bw / ow:.2f} ({bw} words vs {ow} in the source)")
        elif ow > 50 and not 0.95 <= bw / ow <= 1.12:
            notes_only.append(f"{name}: length ratio {bw / ow:.2f}: worth a look (often long NET quotations or omitted glosses)")

        markers = sorted(set(re.findall(r"\[(\d+)\]", orig)), key=int)
        for n in markers:
            if f"[{n}]" not in body:
                problems.append(f"{name}: footnote marker [{n}] missing from the text")
            if not re.search(rf"^\[{n}\]", text, flags=re.M):
                problems.append(f"{name}: note [{n}] missing from the notes")

        for k, line in enumerate(body.split("\n")):
            if line.lstrip().startswith(("*In the margin", ">")):
                continue
            for w in ARCHAIC.findall(KEPT_PHRASES.sub("", line)):
                problems.append(f"{name}: archaic '{w}' in the text: {line.strip()[:80]}")
            if re.match(r"\*\*(Grand )?Direction \d+\.[^*]{3,}\*\*\s*[A-Za-z]", line):
                problems.append(f"{name}: bold Direction heading runs into its paragraph: {line[:70]}")

    ranges.sort()
    for (a1, b1, n1), (a2, b2, n2) in zip(ranges, ranges[1:]):
        if a2 <= b1:
            kind = "duplicate range" if (a1, b1) == (a2, b2) else "overlap"
            problems.append(f"{kind}: {n1} ({a1}-{b1}) and {n2} ({a2}-{b2})")
        elif a2 > b1 + 1:
            gap = src[b1:a2 - 1]
            in_notes = False
            real = []
            for i, line in enumerate(gap, start=b1 + 1):
                if line.strip() == "FOOTNOTES:" or re.match(r"^\[\d+\]", line):
                    in_notes = True
                if line.strip() and not in_notes:
                    real.append(i)
            known = any(g["lines"][0] <= real[0] and real[-1] <= g["lines"][1] for g in vol.get("known_gaps", [])) if real else False
            if real and not known:
                problems.append(f"gap with text between {n1} and {n2}: source lines {real[0]}-{real[-1]}")

    print(f"{len(files)} files checked, covering {sum(b - a + 1 for a, b, _ in ranges)} source lines")
    for p in problems:
        print("  - " + p)
    for p in notes_only:
        print("  ~ " + p)
    print("OK" if not problems else f"{len(problems)} item(s) need attention")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
