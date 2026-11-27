# Working conventions for modernizing sections

This file records how sections are done in practice, so that anyone (or any
agent) doing the next section produces the same kind of file. It applies to
every work in `works/`. `STYLE_GUIDE.md` has the principles, `GLOSSARY.md`
the standing word decisions, and each work's `works/<work>/NOTES.md` the
things particular to that book (its labels, how its footnotes are laid out,
its technical terms, and finished files to imitate). Read all four first.

## What one job is

One file per job, covering a stated line range of the work's source text
(the `source` in its `work.json`). Cover **every sentence** in the range.
Never omit, summarize, or merge. If a passage is skipped for any reason, say
so in the translator's notes.

## File layout

```
---
source: original/<source file>          (relative to the work's folder)
source_lines: START-END
status: draft
modernized: YYYY-MM-DD
---

# <Unit>: <a heading naming what the file covers>

**Direction M. <the Direction's heading sentence(s), in bold, on its own line>**

<body paragraphs, in the author's order>

---

## <Author>'s notes
<each footnote whose marker appears in the range, with its number>

## Translator's notes
<bulleted notes>
```

- The author's numbered headings (Direction, Temptation, Title, Sign, Rule,
  and so on; the work's `NOTES.md` lists them) are bold, with the heading
  sentence on its own line and the body in the next paragraph. Objections,
  Questions, and Answers get italic labels (`*Objection 1.*`, `*Answer.*`).
  Use Arabic numbers for the labels ("Direction 4", not "Direction IV").
  A numbered list stays numbered as the author has it.
- Margin notes (`[Sidenote: ...]` in the source) appear as an italic line
  above their paragraph: `*In the margin: ...*`. Most name the paragraph's
  topic, and the EPUB shows them as small headings.
- Footnote markers keep the author's numbers, with a space before the
  bracket: ` [61]`. Put each footnote under the notes heading with the same
  number, at the start of its line: `[61] text`. Find the text with
  `grep -n '^\[61\]'` on the source.
- If no footnote markers fall in the range, write "None in this section."
- If the range begins or ends partway through a Direction or a list, say so
  in the translator's notes, not in the text. Do not invent a heading.

### No per-file boilerplate

Do not add any of these to individual files; they are said once for the
whole work (in its README, its web page, and its EPUB's "About This Edition"):

- that Scripture is from the NET Bible, a pointer to `NOTICE.md`, or that the
  verses were fetched from labs.bible.org;
- that the Latin translations are drafts that need a Latinist's check, or
  that they were prepared for this project;
- that the notes are "reproduced as in the source," or that English in the
  notes is modernized;
- that the range contains no Latin or Greek.

Write a translator's note only when it says something about *this* passage.
A specific doubt about a particular Latin rendering ("rendered loosely") is
fine.

## How to modernize the words

Follow `STYLE_GUIDE.md` and `GLOSSARY.md`. In practice:

- **Change words, not sentences.** Do not split, merge, reorder, or drop
  sentences. Keep semicolons, colons, question marks, exclamations, and the
  "and... and... and" chains. Only light comma cleanup: drop a comma between
  subject and verb, or before "that/as/when" that completes the clause; leave
  commas that mark a list or a real pause.
- thou/thee/thy/thine and -eth/-est endings become you/your and plain verbs
  (hath to has, doth to does, saith to says, unto to to). Modern spelling,
  American. The one fixed phrase kept is "repentance unto life."
- Replace archaic or shifted-meaning words with the modern equivalent the
  glossary gives. When you meet a word the glossary does not cover and make a
  decision, record it in the translator's notes (the author's word, then
  yours); recurring decisions are moved into the glossary between rounds.
- Keep the author's technical terms that the glossary marks "kept," with a
  note at first use in a file.
- Keep blunt words (whore, dung, harlot) and polemic against Rome and the
  sects exactly as written; add a one-line note that it is the author's
  polemic. Never soften or sharpen.
- Keep the author's book titles in italics.
- When one word is hard, keep it and explain it in the translator's notes, or
  change it and record the swap.

## Scripture

- **Translation: NET Bible.** Where the author *quotes* a verse, use the NET
  wording of that verse, keeping the extent quoted (a phrase stays a phrase;
  use "..." for skips). **Fetch the NET text; never quote it from memory.**

  ```
  curl -sSfG --max-time 20 "https://labs.bible.org/api/" \
    --data-urlencode "passage=Romans 8:7" \
    --data-urlencode "type=text" --data-urlencode "formatting=plain"
  ```

  (Poetry lines can come back run together with no space, like
  "Cleanse yourselves!Remove": add the missing spaces. A bracket such as `]]`
  at the end means the passage is bracketed as a textual variant in the NET;
  mention that in a note.)
- Convert references to modern form: "Rom. viii. 7" becomes "Romans 8:7",
  in parentheses after the quotation; "Matt. xxv." becomes "Matthew 25".
- If the quotation is clearly a **paraphrase or a blend**, keep the author's
  wording, modernized, in quotation marks, cite what is cited, and say in a
  note that it is a paraphrase, giving the NET wording in the note.
- If the author's quoted words are not in the NET verse at all, keep the
  author's wording and flag it in a note.
- **Flag it whenever the NET wording changes the sense the author leans on.**
  Puritans often build on one King James word (zeal, perfection, converting,
  "of the word," "kiss the Son"). Say what the King James had, what the NET
  has, and why it matters to the argument.
- If a printed reference is clearly wrong (a verse that does not exist, or
  does not contain the words), use the correct reference and note the
  correction. If unsure, keep the printed reference and note the doubt.
  **Do not invent references.** A reference the author did not give may go in
  the translator's notes only, marked as not in the text.
- List unmarked Scripture allusions in the translator's notes, keeping the
  author's wording. Do not put a reference in the text that the author did
  not give.

## Latin, Greek, and the author's notes

- The author's footnotes are carried over in full.
- Latin and Greek stay **exactly as printed**, including obvious typos (note
  the typo). After each passage, add a draft English translation in
  parentheses: `(English: ... Author, *Work*.)`. Mark an obscure passage
  "rendered loosely."
- English inside a footnote is modernized like the body.
- A footnote that is only a list of Scripture references is converted to
  modern form (`1 Peter 5:2-4; 2 Corinthians 10:4`).

## What not to assert

- Do not add historical, biographical, or bibliographic claims from memory
  unless you hedge them ("probably," "we have not confirmed"). Prefer saying
  nothing to guessing. The author's own claims about history or the Roman
  Church are kept as the author's and noted as such.
- Do not "fix" the author's argument or grammar beyond the word-level
  conventions above.

## Translator's notes (what to put in them)

Short bullets: NET flags; corrected references; non-obvious word swaps (the
author's word, then yours); technical terms kept; unmarked allusions; source
oddities (misprints, a number out of sequence, garbled syntax); where the file
starts or stops partway; cross-references to other sections that you have not
checked.

## Do not

- Do not edit any other file, run git, or touch a README. One file in, one
  file out. The person coordinating will commit.
