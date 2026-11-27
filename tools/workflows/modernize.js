export const meta = {
  name: 'modernize',
  description: 'Modernize a list of source ranges (one file each), with an optional light review, committing after each wave',
  whenToUse: 'Run with args from tools/plan_jobs.py; see tools/README.md',
  phases: [
    { title: 'Write', detail: 'One writer per range' },
    { title: 'Review', detail: 'Optional light review, one reviewer per three files' },
    { title: 'Checkpoint', detail: 'Commit after each wave' },
  ],
}

// args = {
//   work: 'baxter-christian-directory',          // folder under works/
//   source: 'original/part2-gutenberg-43800.txt', // relative to the work folder
//   out: 'modernized/part2-economics',            // relative to the work folder
//   unit: 'Part 2, Chapter 1',                    // how to name this batch in logs and commits
//   labelling: '...',      // how this chapter's headings, Directions, Objections, etc. are rendered
//   footnotes: '...',      // where the footnote text for this range lives in the source
//   heading: 'Part 2, Chapter 1',  // what each file's "# " heading starts with
//   jobs: [...],           // from tools/plan_jobs.py
//   review: true,          // light review pass after writing (default true)
//   wave: 7,               // writers per wave (default 7)
//   date: '2026-11-27',    // for the front matter
// }
const A = args
const ROOT = '/Users/josh/personal/microprojects/baxter_directory'
const W = 'works/' + A.work
const SRC = W + '/' + A.source
const OUT = W + '/' + A.out
const LOG = W + '/logs/progress-' + A.unit.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '.txt'
const WAVE = A.wave || 7
const REVIEW = A.review !== false

const WRITE_SCHEMA = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    words_original: { type: 'number' },
    words_modernized: { type: 'number' },
    footnotes: { type: 'array', items: { type: 'string' } },
    scripture_flags: { type: 'array', items: { type: 'string' } },
    uncertain: { type: 'array', items: { type: 'string' } },
  },
  required: ['file', 'words_original', 'words_modernized', 'footnotes', 'scripture_flags', 'uncertain'],
}
const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'object', properties: {
      file: { type: 'string' },
      omissions_fixed: { type: 'array', items: { type: 'string' } },
      quotes_fixed: { type: 'array', items: { type: 'string' } },
      other_fixes: { type: 'array', items: { type: 'string' } },
      concerns: { type: 'array', items: { type: 'string' } },
    }, required: ['file', 'omissions_fixed', 'quotes_fixed', 'other_fixes', 'concerns'] } },
  },
  required: ['files'],
}
const CHECKPOINT_SCHEMA = {
  type: 'object',
  properties: { committed: { type: 'boolean' }, hash: { type: 'string' }, note: { type: 'string' } },
  required: ['committed', 'hash', 'note'],
}

const RULES = 'BEFORE YOU WRITE, read these files in ' + ROOT + ' (they are the rules):\n' +
  '  1. CONVENTIONS.md (the practice: file layout, word swaps, Scripture/NET handling, Latin, what not to assert)\n' +
  '  2. STYLE_GUIDE.md and GLOSSARY.md (use the glossary decisions; do not invent a different rendering for a word it covers)\n' +
  '  3. ' + W + '/NOTES.md (this work: its labels, footnote layout, and two or three finished example files to imitate)\n'

function where(job) {
  let s = 'Your range is ' + job.label + ': ' + SRC + ' lines ' + job.start + '-' + job.end + ' (inclusive).'
  if (job.ctx) s += ' The most recent Direction-type heading at or before the start is: "' + job.ctx + '" (a hint only; read the text to see where you are).'
  if (job.part > 1) s += ' The range may begin in the middle of a Direction or a list: if so, do not invent a heading, and say so in the translator\'s notes (not in the text).'
  if (job.part < job.parts) s += ' It may end partway through; the next file continues it.'
  return s
}

function writePrompt(job) {
  return 'You are modernizing one section of a Puritan work in the project at ' + ROOT + '.\n\n' +
  'YOUR JOB: ' + where(job) + '\nRead exactly that range with: sed -n \'' + job.start + ',' + job.end + 'p\' ' + ROOT + '/' + SRC + '\n\n' +
  RULES + '\n' +
  'Key points (details are in CONVENTIONS.md): modernize WORDS only, never split, merge, reorder, or drop sentences; cover every sentence of the range; NET Bible for quoted Scripture, FETCHED from labs.bible.org (never from memory); flag in the translator\'s notes wherever the NET wording changes the sense the author leans on; footnotes carried over in full with draft English translations of any Latin or Greek; hedge or omit any outside claim you are not sure of; no per-file boilerplate (see CONVENTIONS.md).\n\n' +
  'LABELLING FOR THIS UNIT: ' + A.labelling + ' Head the file "# ' + A.heading + ': <short description of this range>".\n\n' +
  'FOOTNOTES: ' + A.footnotes + ' For a marker such as [580] in your range, find its text with grep -n \'^\\[580\\]\' ' + ROOT + '/' + SRC + ' and read to the next numbered note.\n\n' +
  'NO DUPLICATE FILES: first run ls ' + ROOT + '/' + OUT + '/' + job.prefix + '* . If a file with your prefix exists (an earlier attempt at this job), overwrite THAT file. There must be exactly one file with your prefix when you finish.\n\n' +
  'CHECK YOUR OWN WORK before finishing: re-read the source range against your file sentence by sentence and restore anything omitted, merged, or paraphrased; confirm every [n] marker is present; confirm every NET quotation matches what you fetched; delete or hedge any outside claim you are not sure of.\n\n' +
  'STRICTNESS: (a) add no words the author did not write, except where a modern equivalent needs one; explanations go in the translator\'s notes, never in the text; (b) keep word order and sentence boundaries, swapping words in place; (c) do not paraphrase, condense, or drop a clause; (d) do not over-modernize a word that is still ordinary English; (e) never quote the NET from memory; (f) keep every [n] marker where it falls.\n\n' +
  'OUTPUT: write exactly ONE file, ' + ROOT + '/' + OUT + '/' + job.prefix + '<slug>.md, where <slug> describes the content (lowercase, hyphens, under 60 characters). Front matter: source: ' + A.source + ', source_lines: ' + job.start + '-' + job.end + ', status: draft, modernized: ' + A.date + '. Edit no other file except to append one line: echo "written: <your file>" >> ' + ROOT + '/' + LOG + '. Do not run git. Other agents are writing other files at the same time.\n\n' +
  'Then count words (sed -n \'' + job.start + ',' + job.end + 'p\' ' + ROOT + '/' + SRC + ' | wc -w, and wc -w on your file\'s text) and return the structured result.'
}

function reviewPrompt(group) {
  const list = group.map((g) => '  - ' + g.file + '  (source lines ' + g.job.start + '-' + g.job.end + ')').join('\n')
  return 'You are doing a LIGHT REVIEW of draft modernizations in the project at ' + ROOT + '. Catch and fix clear errors; do not restyle.\n\n' +
  'FILES (compare each with its range of ' + ROOT + '/' + SRC + '; read a range with sed -n \'S,Ep\'):\n' + list + '\n\n' +
  RULES + '\nFor each file check:\n' +
  '1. COMPLETENESS: walk the source paragraph by paragraph; restore any sentence, clause, numbered point, margin note, objection, or answer that is missing, merged, or summarized, and restore sentence boundaries.\n' +
  '2. SCRIPTURE: fetch every verse presented as NET wording and compare: curl -sSfG --max-time 20 "https://labs.bible.org/api/" --data-urlencode "passage=Romans 8:7" --data-urlencode "type=text" --data-urlencode "formatting=plain" . Fix misquotations; check references are modern and none is invented.\n' +
  '3. FOOTNOTES: every [n] marker in the range is in the file with its full note (' + A.footnotes + ').\n' +
  '4. WORDS: no leftover archaisms; glossary decisions followed; no obvious mistranslation of a shifted word.\n' +
  '5. NOTES: delete or hedge any historical or bibliographic claim stated as fact without support.\n\n' +
  'Fix only real errors, with the Edit tool. Edit only these files, except to append one line per file: echo "reviewed: <file>" >> ' + ROOT + '/' + LOG + '. Do not run git. Return what you fixed and any concern you could not resolve (empty arrays are fine).'
}

function checkpointPrompt(msg) {
  return 'In the git repository at ' + ROOT + ', run exactly these commands and nothing else (except `git status --short | head` if one fails):\n' +
  '  git add ' + OUT + ' ' + LOG + '\n' +
  '  git commit -q -m "' + msg + '" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"\n' +
  '"nothing to commit" is fine. Then run git log --oneline -1 and return whether a commit was made, the short hash, and a one-line note.'
}

const waves = []
for (let i = 0; i < A.jobs.length; i += WAVE) waves.push(A.jobs.slice(i, i + WAVE))
const written = []
const reviewed = []
const missing = []
for (let w = 0; w < waves.length; w++) {
  log(A.unit + ': wave ' + (w + 1) + ' of ' + waves.length)
  const res = await parallel(waves[w].map((job) => () =>
    agent(writePrompt(job), { label: 'write ' + job.id, phase: 'Write', schema: WRITE_SCHEMA })))
  const ok = []
  res.forEach((r, i) => { if (r && r.file) { ok.push({ job: waves[w][i], file: r.file, result: r }) } else missing.push(waves[w][i].id) })
  written.push(...ok)
  if (REVIEW && ok.length) {
    const groups = []
    for (let i = 0; i < ok.length; i += 3) groups.push(ok.slice(i, i + 3))
    const rv = await parallel(groups.map((g, i) => () =>
      agent(reviewPrompt(g), { label: 'review ' + g[0].job.id, phase: 'Review', schema: REVIEW_SCHEMA })))
    rv.forEach((r) => { if (r) reviewed.push(...r.files) })
  }
  const cp = await agent(checkpointPrompt('Checkpoint: ' + A.unit + ' wave ' + (w + 1) + ' of ' + waves.length + (REVIEW ? ' written and reviewed' : ' written')),
    { label: 'checkpoint wave ' + (w + 1), phase: 'Checkpoint', schema: CHECKPOINT_SCHEMA, effort: 'low' })
  log('Checkpoint: ' + (cp ? cp.hash + ' ' + cp.note : 'no result'))
}
if (missing.length) log('Ranges with no file: ' + missing.join(', '))
return { unit: A.unit, jobs: A.jobs.length, written: written.map((x) => x.result), reviewed, missing }
