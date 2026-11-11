# Contributor guide — Second Reading

Read this before changing anything. It applies to people and to AI assistants
working on the site from any chat.

## What the site is

*Second Reading* publishes annotated editions of recorded talks and lectures.
Each edition fills the gaps in what the speaker says, checks claims against
sources, adds precise dates, footnotes, links, pictures and drawings.
Language: **English**.

## How it is built

- [Quarto](https://quarto.org) website. Pages are `.qmd` files (Markdown).
- Every push to `main` triggers `.github/workflows/publish.yml`, which renders
  the site and deploys it to GitHub Pages: <https://saintemmma-stack.github.io>.
- To preview locally: `quarto preview` (or `pip install quarto-cli` first).

```
_quarto.yml                  site settings, navigation, theme
index.qmd                    home page: the library list
about.qmd                    about, sourcing policy, rights
assets/                      theme (light.scss, dark.scss, common.scss), fonts, note popovers
works/<slug>/index.qmd       one folder per work
works/<slug>/images/         images for that work, each with a credit
```

## Adding a new work

1. Create `works/<short-slug>/index.qmd` (lowercase, hyphens).
2. Add an entry to the `<ul class="sr-library">` list in `index.qmd`.
3. Front matter: `title`, `subtitle` (speaker, date, what the edition is), `date-modified: last-modified`.
4. While unfinished, start the page with a `::: {.sr-status}` line saying what is done.
5. A multi-chapter work (a lecture series) gets one folder with one `.qmd` per chapter
   and an `index.qmd` table of contents.

## Writing conventions

**Tone.** Clear, scholarly, never stiff. Personal remarks are welcome when they
add something (an irony, a judgement, a connection), but phrased as the edition's
judgement, not as invented personal experience: write "There is an irony here",
not "I was surprised to find".

**The speaker's words.** Quote them briefly in a blockquote, each preceded by a
timestamp link to the recording:

```markdown
::: {.sr-ts}
[00:34 in the video](https://www.youtube.com/watch?v=VIDEO_ID&t=34s)
:::

> Short quoted passage.
```

Do not publish full transcripts of copyrighted talks; quote what the commentary
needs and paraphrase the rest. Full transcripts are kept privately, outside this
public repository.

**No verdict labels.** Do not tag claims as "accurate" or "wrong"; let the notes show it.

**Footnotes** are for sources and precise details. Use named Pandoc footnotes
(`[^short-name]`), collected at the end of the file. On the site, clicking a
note number opens the note next to the text. Each note gives full bibliographic
details and, where possible, a link.

**Inline links** are for explanations: a link on the name of an event, person or
work, to a page that explains it to a curious reader.

**"For the curious" boxes** suggest further reading at the end of a section:

```markdown
<details class="curious">
<summary>For the curious</summary>

- **Topic.** One line saying why this source is worth reading, with the link.

</details>
```

**Dates.** Be precise (day, month, year) when the source allows it. When sources
disagree, say so in a note.

## Sources

Every factual claim must rest on a source that was actually checked. In order of
preference: primary sources → scholarship → reference works and institutions →
general overviews (Wikipedia: fine as a first link, never the only support for a
contested claim). Only link URLs that were verified to exist and to say what the
note claims.

## Images and drawings

- **Photos and portraits:** only from collections that allow reuse (Wikimedia
  Commons, public-domain archives such as US government works, CC-licensed
  collections). Avoid "fair use" images from Wikipedia: they cannot be reused.
- Save images in `works/<slug>/images/`. Under each image, give a caption with
  the credit and licence exactly as the source asks (Commons: the "Use this
  file" button gives the line).
- A slot still waiting for a picture is marked with:

```markdown
::: {.todo-figure}
[Photo to add]{.todo-label}
What the picture should show, and a suggested source.
:::
```

- **Drawings** (timelines, maps, diagrams) are original inline SVGs inside
  `<figure class="sr-drawing">`. Use the classes `ink`, `graphite`, `pencil`
  (fills) and `stroke-ink`, `stroke-pencil` (strokes) so they follow light and
  dark mode. Wide drawings go inside `<div class="sr-scroll">`.

## Design

One signature element, the editor's blue pencil: the underline on the home
title, circled note numbers, and the bracket beside quotations. Literata for
reading; Schibsted Grotesk for interface text (navigation, captions, timestamps).
Keep everything else quiet. Do not add new colours or fonts without a reason.
