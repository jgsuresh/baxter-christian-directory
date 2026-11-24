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
- His quotations are from the KJV or his own paraphrase. Keep a quoted verse
  close to the KJV wording when he quotes it, and modernize only
  the words that are archaic (e.g., "thee"); leave a reference to the
  original text in a note if he paraphrases loosely.

## Notes and marks

- Baxter's own footnote numbers from the Gutenberg text (e.g. `[7]`) are kept
  if the footnote is carried over.
- Our notes use `[Note: …]` in the text or a "Translator's notes" section at
  the end of each file. Notes are for: shifted word meanings, historical
  context, dated claims (medical, social), and places where we chose between
  two readings.
- Never silently omit anything. If a passage is skipped or abridged, say so.

## File layout

- `modernized/part1-ethics/chNN-short-title.md` etc.
- Each file starts with front matter: source file, line range in the Gutenberg
  text, status (`draft` | `reviewed`), date.
- Samples live in `modernized/samples/` until a passage is accepted into the
  main sequence.
