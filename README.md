# Puritan Works, Modernized

Puritan books rendered into modern English one word at a time. The author's
sentences, order, and argument are kept exactly; only words that have aged
are changed: *thou* and *hath*, old spellings, and words whose meaning has
shifted. Everything we add is free to use (CC0).

Read and download: <https://jgsuresh.github.io/texts/>. Found a mistake?
[Open an issue](https://github.com/jgsuresh/puritan-modernized/issues/new).

## Works

| Work | Author | Status | Folder |
|---|---|---|---|
| *A Christian Directory* (1673) | Richard Baxter | Part 1 of 4 drafted | [`works/baxter-christian-directory`](works/baxter-christian-directory) |

## How the repository is laid out

| Path | What it holds |
|---|---|
| `STYLE_GUIDE.md` | The principles every modernization follows. |
| `CONVENTIONS.md` | The practice: file layout, Scripture and Latin handling, notes. |
| `GLOSSARY.md` | Standing word decisions, shared by all works. |
| `NOTICE.md`, `LICENSE` | Licensing (CC0 for our additions; NET Bible terms for Scripture). |
| `tools/` | Planning, checking, EPUB building, and the writing workflow. See [`tools/README.md`](tools/README.md). |
| `works/<work>/` | One folder per work: `original/` (untouched source texts), `modernized/` (the modernized files), `work.json` (settings), `NOTES.md` (what is particular to the work), `logs/`, `docs/`. |

## Licensing

The original texts are in the public domain; the Project Gutenberg files in
each `original/` folder keep Gutenberg's header and its terms. The modernized
text, notes, glossary, guides, and tools are dedicated to the public domain
under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (see
`LICENSE`). Scripture quotations are from the NET Bible® and are not covered
by CC0; see [NOTICE.md](NOTICE.md).
