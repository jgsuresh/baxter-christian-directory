# Modernization Style Guide

These principles apply to every work in this repository. Examples are drawn
from Baxter's *Christian Directory*, the first work done.

Goal: a faithful rendering that a modern reader, a counselor or pastor
especially, can read without a dictionary, while still sounding like the
author (for Baxter: direct, urgent, pastoral).

## Principles

1. **Faithful over fashionable.** Preserve the author's meaning, argument order,
   and emphasis. Don't soften, sharpen, or editorialize. If a passage is
   uncomfortable to modern ears, render it accurately and add a note rather
   than quietly changing it.
2. **Keep the structure.** Keep the author's numbered divisions (for Baxter:
   Directions, Objections and Answers, Parts, and Titles), spelling out
   abbreviated labels (*Direct.*, *Object.*, *Answ.*) as "Direction",
   "Objection", "Answer", with the same numbering.
3. **Modernize words, not sentences.** (Decided after sample round 1.) Keep
   the author's sentence boundaries, punctuation, clause order, and lists. Change
   only archaic or shifted-meaning words, spelling, and the small grammar
   that follows from them. Do not split, merge, or reorder sentences.
4. **Keep the voice.** Keep the author's imperatives, rhetorical questions, and
   exclamations. Tone down only archaisms that obscure meaning.

## Language

- **Pronouns and verbs:** thou/thee/thy/thine and -eth/-est endings become
  you/your and plain verbs. "Take heed" → "Be careful" or "Watch out" as
  context requires.
- **Words that changed meaning** (the big risk): render the sense the author
  meant, not the sense we'd assume. Examples to watch: *conversation*
  (conduct), *carnal* (fleshly/unspiritual), *sensual* (of the senses, not only
  sexual), *affections* (emotions/desires), *convince* (prove wrong),
  *prevent* (go before), *suffer* (allow), *religion* (worship and devotion),
  *melancholy* (a long-lasting low or fearful mood, tied in his day to bodily
  "humors"). Maintain a running glossary in `GLOSSARY.md`.
- **Theological terms stay:** justification, sanctification, regeneration,
  covenant, grace, etc. Explain in a note only if the author uses one in
  an unusual way.
- **Gendered language:** keep the author's "man/men" where he means people
  generally if the sense is clear; use "people" where "men" would mislead.
  Don't remove references to women, wives, and husbands; where his
  generalizations about groups read as dated, translate faithfully and note.
- **Spelling:** American spelling.
- **Punctuation (light touch):** change a mark only where it reflects
  17th-century convention rather than meaning. Allowed: drop a comma that
  separates a subject from its verb or a clause from the "that"/"as"/"when"
  it completes; replace Gutenberg's `--` run-in marks with a bold heading;
  fix quotation marks, parentheses, and italics. Not allowed: turning
  semicolons or colons into periods, adding or removing a sentence boundary,
  or touching the "and… and… and" chains, exclamations, or questions. If a
  comma change would commit us to one reading of ambiguous grammar, leave
  the author's mark and add a note.

## Scripture

- Puritan authors cite in "Isa. lv. 1-3" style. Convert to "Isaiah 55:1–3".
- **Translation: NET Bible®.** Puritans quote the King James Version (or the
  Geneva Bible), often loosely or in fragments. Where they quote a verse, use the NET wording of
  that verse, keeping the extent of what is quoted (a phrase stays a phrase;
  use "..." for skips). Fetch the text; do not quote it from memory.
  The author's own prose around the quotation is modernized as usual.
- If the author paraphrases rather than quotes, keep the paraphrase, modernized, and
  say so in the translator's notes.
- Note it when the NET wording changes the sense the author is leaning on (for
  example "narrow door" for "strait gate").
- Verse text and its NOTICE terms: see [NOTICE.md](NOTICE.md).
- **Misprinted references:** if a reference is clearly wrong in the source
  text (for example "Heb. xxi. 14," where Hebrews has 13 chapters), use the
  correct one and say so in the translator's notes.

## Notes and marks

- The author's own footnote numbers from the source (e.g. `[7]`) are kept and
  the footnotes are carried over under "<Author>'s notes." Latin stays
  verbatim with a draft English translation in parentheses after each
  passage; English in the notes is modernized like the body.
- Our notes go in a "Translator's notes" section at the end of each file,
  never in the text. Notes are for: shifted word meanings, historical
  context, dated claims (medical, social), and places where we chose between
  two readings.
- Never silently omit anything. If a passage is skipped or abridged, say so.

## File layout

- Each work lives in `works/<author>-<short-title>/`, with its source texts in
  `original/`, the modernized files in `modernized/<volume>/`, its settings in
  `work.json`, and what is particular to it in `NOTES.md`.
- One file per section (an opening address, a numbered list, or one or more
  Directions), named so that the files sort in reading order, for example
  `ch03-09-p2-....md`. Front matter gives the source file, its line range,
  status (`draft` | `reviewed`), and the date. See `CONVENTIONS.md`.
