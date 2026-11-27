# Tools

Everything here runs from the repository root. Python scripts need only the
standard library, except `build_epub.py`, which `uv run` sets up itself.

## The round for one chapter (or other unit)

1. **Find the sections.** Read the source and note the first line of each
   natural section (a Title, a Part, a run of Directions) and the chapter's
   last line: `grep -n` for `CHAPTER`, `_Tit._`, `PART`, `_Direct._`, `FOOTNOTES:`.

2. **Plan the jobs.** Split the chapter into files of about 190 source lines,
   cut at paragraph boundaries:

   ```bash
   python3 tools/plan_jobs.py baxter-christian-directory part2 --chapter 1 \
     --section 120 "Chapter title and Directions 1-10" \
     --section 980 "Directions 11-20" --end 5123 > /tmp/jobs.json
   ```

3. **Write (and review).** Run `tools/workflows/modernize.js` with the Workflow
   tool, passing `args` with the jobs and the unit's labelling instructions
   (the header of the script lists every argument). Writers follow
   `CONVENTIONS.md`, `STYLE_GUIDE.md`, `GLOSSARY.md`, and the work's
   `NOTES.md`; a light review (one reviewer per three files) follows each wave
   unless `review: false`; each wave is committed.

4. **Check.** Fix anything listed, then rerun until it says OK:

   ```bash
   python3 tools/check.py baxter-christian-directory part2 --prefix ch01-
   ```

5. **Glossary.** Add any word decision that came up more than once to
   `GLOSSARY.md`.

6. **Build the book** when a volume (or a useful part of one) is done; the
   volume needs `epub` settings in `work.json`:

   ```bash
   uv run tools/build_epub.py baxter-christian-directory part1
   ```

   The EPUB goes to `dist/` (not committed). Publish it as a GitHub release
   whose asset name matches the web page's download link.

## Scripts

| File | What it does |
|---|---|
| `plan_jobs.py` | Splits sections of a source into writer jobs (JSON). |
| `workflows/modernize.js` | Writer agents, optional light review, and a commit after each wave. |
| `check.py` | Coverage, duplicates, length ratio, footnotes, archaisms, headings. |
| `build_epub.py` | Builds a Kindle-friendly EPUB of one volume from `work.json`. |

## Adding a new work

1. Make `works/<author>-<short-title>/` with `original/` (the source text,
   unedited) and `modernized/<volume>/`.
2. Write `work.json` (copy Baxter's: title, author, edition, volumes with
   `source` and `dir`) and `NOTES.md` (the author's labels, footnote layout,
   technical terms; after the first round, two or three finished files to
   imitate).
3. Do a short sample round first (`docs/style-samples/`) to check that the
   shared rules suit the author, and record anything particular in `NOTES.md`.
4. Add the work to the table in the top-level `README.md`, and give it a page
   on the website.
