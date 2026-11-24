# Working conventions for modernizing sections

This file records how sections have actually been done so far, so that anyone
(or any agent) doing the next section produces the same kind of file.
`STYLE_GUIDE.md` has the principles; this file has the practice.
For worked examples, read two or three finished files in
`modernized/part1-ethics/`, for instance:
`ch02-06-direction-06-do-not-be-discouraged-by-difficulties.md`,
`ch02-07-direction-07-live-under-a-faithful-minister.md`,
`ch01-part1-12-direction-09-the-misery-of-an-unconverted-state.md`.

## What one job is

One file per job, covering a stated line range of
`original/part1-gutenberg-41633.txt`. Cover **every sentence** in the range.
Never omit, summarize, or merge. If a passage is skipped for any reason, say
so in the translator's notes.

## File layout

```
---
source: original/part1-gutenberg-41633.txt
source_lines: START-END
status: draft
modernized: 2026-11-24
---

# Chapter N: Direction M            (or a heading naming what the file covers)

**Direction M. <the Direction's heading sentence(s), bold>**

<body paragraphs, in Baxter's order>

---

## Baxter's notes
<each footnote whose marker appears in the range, with its number>

## Translator's notes
<bulleted notes>
```

- Directions, Temptations, Objections, and Answers are labelled in bold
  (`**Direction 8.**`, `**Temptation 3.**`) or italic (`*Objection.*`,
  `*Answer.*`) the way the finished files do. Baxter's margin summaries
  (`[Sidenote: ...]` in the source) appear as an italic line above the
  paragraph: `*In the margin: ...*`. A numbered Baxter list stays numbered.
- Footnote markers keep Baxter's numbers: ` [61]` (a space before the
  bracket). Put each footnote under "Baxter's notes" with the same number.
  Footnote text is in the `FOOTNOTES:` block at the end of the chapter in the
  source (for Chapter 2, lines 8532-8780). Find it with
  `grep -n '^\[61\]'`.
- If no footnote markers fall in your range, write "None in this section."

## How to modernize the words

Follow `STYLE_GUIDE.md` and `GLOSSARY.md`. In practice:

- **Change words, not sentences.** Do not split, merge, reorder, or drop
  sentences. Keep semicolons, colons, question marks, exclamations, and the
  "and... and... and" chains. Only light comma cleanup: drop a comma between
  subject and verb, or before "that/as/when" that completes the clause; leave
  commas that mark a list or a real pause.
- thou/thee/thy/thine and -eth/-est endings become you/your and plain verbs
  (hath to has, doth to does, saith to says). Modern spelling, American.
- Replace archaic or shifted-meaning words with modern equivalents. Decisions
  already made (use them): infidel to unbeliever; sensual to
  physical / pleasure-loving / "indulgence in physical pleasure" (by context);
  sensualists to pleasure-seekers; sensitive (appetite, faculties) to sensory;
  covetous(ness) to greedy / greed; conversation (conduct) to conduct;
  pretend (claim) to claim; endeavor to effort; felicity to happiness;
  concernment to concern; conceit(s) to notion(s); vanity/vain (empty) to
  empty / worthless; sports to amusements; carnal stays; mortify stays;
  holy ghost to Holy Spirit; Saviour to Savior; honour to honor;
  prevailing/prevalent to powerful or successful; presently to at once;
  suffer (allow) to allow; convince stays when it means persuade;
  discourse (talk) to talk or conversation; amiable to lovable;
  wilful to willful; scarce to scarcely; whither/thither to where/there.
  Keep these as Baxter's technical terms, with a note at first use:
  reigning sin, mortal/venial, divinity, assize(s), cases of conscience,
  security (careless confidence), opinionists, formalists, enthusiasts,
  papist (his word for a Roman Catholic), the Indians (Acosta's word for the
  native peoples of the Americas).
- Keep Baxter's blunt words (whore, dung, harlot) and his polemic against
  Rome and the sects exactly as he wrote it; add a one-line note that it is
  his polemic. Never soften or sharpen.
- Keep his own book titles in italics (*Saints' Rest*, *Directions for a
  Sound Conversion*, *Treatise of Conversion*).
- When one word is hard, keep it and explain it in the translator's notes,
  or change it and record the swap in the notes (Baxter's word, then yours).

## Scripture

- **Translation: NET Bible.** Where Baxter *quotes* a verse, use the NET
  wording of that verse, keeping the extent he quotes (a phrase stays a
  phrase; use "..." where he skips). **Fetch the NET text; never quote it
  from memory.** Example:

  ```
  curl -sSfG --max-time 20 "https://labs.bible.org/api/" \
    --data-urlencode "passage=Romans 8:7" \
    --data-urlencode "type=text" --data-urlencode "formatting=plain"
  ```

  (Poetry lines can come back run together with no space, like
  "Cleanse yourselves!Remove": add the missing spaces. A bracket such as `]]`
  at the end means the passage is bracketed as a textual variant in the NET;
  mention that in a note.)
- Convert references to modern form: "Rom. viii. 7" becomes "Romans 8:7";
  put them in parentheses after the quotation; "Matt. xxv." becomes
  "Matthew 25".
- If Baxter's quotation is clearly a **paraphrase or a blend** of verses, keep
  his wording, modernized, in his quotation marks, cite what he cites, and say
  in a note that it is his paraphrase. Put the NET wording in the note.
- If Baxter's own quoted words are not in the NET verse at all (the NET reads
  a different point), keep Baxter's wording and flag it in a note (see
  Psalm 10:4 in `ch01-part2-12-...` for how).
- **Flag it in the translator's notes whenever the NET wording changes the
  sense Baxter is leaning on.** He often builds on one King James word
  (zeal, perfection, converting, "of the word," "kiss the Son"). Say what the
  King James had, what the NET has, and why it matters to his argument.
- If a printed reference is clearly wrong (a verse that does not exist, or
  that does not contain the quoted words), use the correct reference and note
  the correction. If you are not sure, keep Baxter's reference and note the
  doubt. **Do not invent references.** If a quotation has no reference in the
  source, you may add one in the translator's notes only, marked as not in
  Baxter's text.
- List unmarked Scripture allusions in the translator's notes, keeping
  Baxter's wording. Do not put a reference in the text that he did not give.

## Latin, Greek, and Baxter's notes

- Baxter's footnotes are carried over in full, under "Baxter's notes."
- Latin and Greek stay **exactly as printed**, including obvious typos (note
  the typo). After each passage, add a draft English translation in
  parentheses: `(English: ... Author, *Work*.)`. Say once at the top of the
  notes that the translations are drafts prepared for this project and need a
  Latinist's check. Mark an obscure passage "rendered loosely."
- English inside a footnote is modernized like the body.
- A footnote that is only a list of Scripture references is converted to
  modern form (`1 Peter 5:2-4; 2 Corinthians 10:4`).

## What not to assert

- Do not add historical, biographical, or bibliographic claims from your own
  memory unless you hedge them ("probably," "we have not confirmed"). Prefer
  saying nothing to guessing. Baxter's own claims about history or the Roman
  Church are kept as his and noted as his.
- Do not "fix" Baxter's argument or his grammar beyond the word-level
  conventions above.

## Translator's notes (what to put in them)

Short bullets: the NET flags (above); corrected references; every non-obvious
word swap (Baxter's word then yours); technical terms kept; unmarked
allusions; source oddities (misprints, a number out of sequence, garbled
syntax); cross-references to other sections that you have not checked.

## Do not

- Do not edit any other file, run git, or touch README. One file in, one file
  out. The person coordinating will commit.
