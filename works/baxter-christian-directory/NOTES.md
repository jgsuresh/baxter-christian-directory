# Notes for Baxter's *A Christian Directory*

What is particular to this work. The shared rules are in `CONVENTIONS.md`,
`STYLE_GUIDE.md`, and `GLOSSARY.md` at the top of the repository.

## The work

- Richard Baxter, *A Christian Directory, or, A Sum of Practical Theology and
  Cases of Conscience* (1673), in four Parts: 1 Christian Ethics (private
  duties), 2 Christian Economics (family duties), 3 Christian Ecclesiastics
  (church duties), 4 Christian Politics (duties to rulers and neighbors).
- Source: the Project Gutenberg transcriptions of the 1846 edition, one file
  per Part, in `original/` (do not edit them). `work.json` lists them.
- The author's notes heading in each file is `## Baxter's notes`.

## Baxter's labels and how to render them

| In the source | In the modernized file |
|---|---|
| `_Direct._ IV.` | `**Direction 4. <its heading sentence>**` on its own line, body below |
| `Grand Direct. II.` (Part 1, Chapter 3) | `**Grand Direction 2. <heading sentence>**` |
| `_Tit._ 3.` | `**Title 3. <its heading>**` on its own line. "Tit." is Baxter's "Title," a main division of a chapter; say so once per chapter in the notes. |
| `PART II.` inside a chapter | `**Part 2.**` and its sub-heading as a bold line |
| `_Tempt._ 5.` | `**Temptation 5.**` then the text |
| `Sign`, `Rule`, `Motive`, `Thief`, `Instance` | bold label with an Arabic number, as Direction |
| `_Object._`, `_Quest._`, `_Answ._` | `*Objection 1.*`, `*Question 2.*`, `*Answer.*` |
| `[Sidenote: ...]` | `*In the margin: ...*` above its paragraph |

## Footnotes

Each chapter's footnotes are collected in a `FOOTNOTES:` block at the end of
the chapter in the source, numbered continuously through the Part (Part 1
runs [1]-[613]). Find one with `grep -n '^\[61\]'` on the source and read to
the next numbered note; some are long English notes mixed with Latin.

## Technical terms Baxter uses (kept, with a note at first use in a file)

reigning sin; mortal and venial; divinity (theology); assize(s); cases of
conscience; security (careless confidence); opinionists, formalists,
enthusiasts; papist (his word for a Roman Catholic); the Indians (Acosta's
word for the native peoples of the Americas); calling (one's vocation or
occupation); school divinity (the academic theology of the day).

## Finished files to imitate

- `modernized/part1-ethics/ch02-06-direction-06-do-not-be-discouraged-by-difficulties.md`
- `modernized/part1-ethics/ch05-04-p1-title-3-practical-directions-1-6.md`
- `modernized/part1-ethics/ch09-03-p2-questions-10-11-what-a-lie-is-direction-01.md`

(Older Part 1 files still carry per-file boilerplate in their notes, which
`CONVENTIONS.md` now says to leave out; do not copy that.)

## Known oddities

- `work.json` lists gaps between files that are not missing text
  (`known_gaps`), with the reason for each.
- Part 1, Chapter 8 has no Part 7: the source numbers its Parts 1-6, then 8.
