---
name: dev-diary
description: >-
  Convert a Cold War 1970 mod dev diary .docx into a publish-ready Markdown post
  (docs/dev_diaries/NNN-slug.md plus images), with headers and images placed in reading
  order and the author's voice preserved. Use when given a dev-diary .docx to format or
  publish, or "dev diary 7"-style numbering.
---

# Dev Diary to Markdown

The job is structure, not editing. Scaffold the post and place the images. Leave the
author's prose as written. Upstream MD publishes `.mdx` to its docs site; this fork has
no docs site, so the output is plain Markdown that renders on GitHub and can be pasted
into Steam or Discord.

## Preserve the author's voice

- Do not proofread, normalize, reword, reorder, or delete text.
- Keep casual spellings, run-on sentences, asides, jokes, smart quotes, and the
  author's own hyphenation. Keep stylistic ellipses (`….`, `....`) exactly.
- The only allowed change to source text is splitting a paragraph at a sentence
  boundary so an image can sit beside the passage it illustrates.
- Convert an em dash in the source to a period, comma, or colon.
- Text you author (headers, alt text) uses no em dash and no `...`.
- Proofreading is a separate task, only on request, with every change listed.
- English only. If the source is in another language, ask before translating.

## 1. Get the `.docx`

Use the path in `$ARGUMENTS` or the attached file. Otherwise ask for it before doing
anything else. A Google Doc exports with Download, Microsoft Word (.docx). Reject other
formats.

## 2. Number

Take the highest `NNN-` prefix in `docs/dev_diaries/*.md`, add 1, and zero-pad to 3
digits (start at `001` if the folder does not exist). Warn if
`docs/dev_diaries/images/<NNN>/` exists.

## 3. Extract

```bash
python -X utf8 .claude/skills/dev-diary/extract_docx.py \
  --docx "<path to .docx>" \
  --image-dir docs/dev_diaries/images/<NNN>
```

It copies every embedded image, in document order, to `picture-1.png`, `picture-2.png`,
and so on, and prints JSON with `title`, `blocks` (`heading`, `para`, and `image`
entries in source order), and `images`.

## 4. Header

Ask for what cannot be derived, offering defaults:

- Title: the JSON title or first heading, as `Dev Diary #N: <Title>` with N unpadded.
- Author: the real developer handle, not the in-character narrator.
- Mod version the diary refers to (default: the top heading in `Changelog.txt`).
- Date: default today, `YYYY-MM-DD`.

The slug is the kebab-cased title without the `Dev Diary #N:` prefix. The filename is
`docs/dev_diaries/<NNN>-<slug>.md`.

## 5. Assemble

Write the file UTF-8 without BOM:

```md
# Dev Diary #7: Iceland and the Cod Wars

_By Author, 12 June 2026. Mod version v0.3._

<body>
```

- One `#` title only. Keep the intro and sign-off without headers. Add `##` or `###`
  only at real topic shifts. Honor the docx's heading styles. For flat prose, add
  headers in the diary's own wording.
- Every extracted image goes into the body. Place each one right after the sentence
  that introduces it, following the prose cues ("the first picture shows", "the next
  pictures in order are"). Word often dumps all screenshots at the top, so prefer the
  cues over block position.
- When one paragraph describes two visuals, split it so each image sits with its
  passage.
- With no cue, place the image where it sits in the `blocks` order and report it.
- Image form, relative to the post: `![picture1](images/<NNN>/picture-1.png)`.

## 6. Report

- The `.md` path and the image folder.
- How many images were placed, and which had no cue.
- A reminder to check author, version, and date.
- Images over about 2 MB that may need compressing before upload, since the repository
  stores large assets with Git LFS.
