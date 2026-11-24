# Modernization Style Guide (draft)

Goal: a faithful rendering that a modern reader, a counselor or pastor
especially, can read without a dictionary, while still sounding like Baxter:
direct, urgent, pastoral.

## Principles

1. **Faithful over fashionable.** Preserve Baxter's meaning, argument order,
   and emphasis. Don't soften, sharpen, or editorialize. If a passage is
   uncomfortable to modern ears, render it accurately and add a note rather
   than quietly changing it.
2. **Keep the structure.** Keep his numbered Directions, Objections and
   Answers, Parts, and Titles. Use his labels (*Direct.*, *Object.*, *Answ.*)
   as "Direction", "Objection", "Answer", with the same numbering.
3. **Modernize words, not sentences.** (Decided after sample round 1.) Keep
   Baxter's sentence boundaries, punctuation, clause order, and lists. Change
   only archaic or shifted-meaning words, spelling, and the small grammar
   that follows from them. Do not split, merge, or reorder sentences.
4. **Keep the voice.** Keep his imperatives, rhetorical questions, and
   exclamations. Tone down only archaisms that obscure meaning.

## Language

- **Pronouns and verbs:** thou/thee/thy/thine and -eth/-est endings become
  you/your and plain verbs. "Take heed" → "Be careful" or "Watch out" as
  context requires.
- **Words that changed meaning** (the big risk): render the sense Baxter
  meant, not the sense we'd assume. Examples to watch: *conversation*
  (conduct), *carnal* (fleshly/unspiritual), *sensual* (of the senses, not only
  sexual), *affections* (emotions/desires), *convince* (prove wrong),
  *prevent* (go before), *suffer* (allow), *religion* (worship and devotion),
  *melancholy* (a long-lasting low or fearful mood, tied in his day to bodily
  "humors"). Maintain a running glossary in `GLOSSARY.md`.
- **Theological terms stay:** justification, sanctification, regeneration,
  covenant, grace, etc. Explain in a note only if Baxter uses one in an
  unusual way.
- **Gendered language:** keep Baxter's "man/men" where he means people
  generally if the sense is clear; use "people" where "men" would mislead.
  Don't remove his references to women, wives, and husbands; where his
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
  Baxter's mark and add a note.

## Scripture

- Baxter cites by "Isa. lv. 1-3" style. Convert to "Isaiah 55:1–3".
- **Translation: NET Bible®.** Baxter quotes the King James Version, often
  loosely or in fragments. Where he quotes a verse, use the NET wording of
  that verse, keeping the extent of what he quotes (a phrase stays a phrase;
  use "..." where he skips). Fetch the text; do not quote it from memory.
  Baxter's own prose around the quotation is modernized as usual.
- If he paraphrases rather than quotes, keep his paraphrase, modernized, and
  say so in the translator's notes.
- Note it when the NET wording changes the sense he is leaning on (for
  example "narrow door" for "strait gate").
- Verse text and its NOTICE terms: see [NOTICE.md](NOTICE.md).
- **Misprinted references:** if a reference is clearly wrong in the 1846
  text (for example "Heb. xxi. 14," where Hebrews has 13 chapters), use the
  correct one and say so in the translator's notes.

## Notes and marks

- Baxter's own footnote numbers from the Gutenberg text (e.g. `[7]`) are kept
  and the footnotes are carried over under "Baxter's notes." Latin stays
  verbatim with a draft English translation in parentheses after each
  passage; English in his notes is modernized like the body.
- Our notes use `[Note: …]` in the text or a "Translator's notes" section at
  the end of each file. Notes are for: shifted word meanings, historical
  context, dated claims (medical, social), and places where we chose between
  two readings.
- Never silently omit anything. If a passage is skipped or abridged, say so.

## File layout

- `modernized/part1-ethics/chNN-partN-NN-short-title.md` etc., one file per
  section (an opening address, a numbered list, or a single Direction),
  numbered in reading order. The Introduction is `00-introduction.md`.
- Each file starts with front matter: source file, line range in the Gutenberg
  text, status (`draft` | `reviewed`), date.
- Samples live in `modernized/samples/` until a passage is accepted into the
  main sequence.
