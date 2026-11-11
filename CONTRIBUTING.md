# Contributor guide — Second Reading

Read this before changing anything. It applies to people and to AI assistants
working on the site from any chat.

## What the site is

*Second Reading* publishes annotated editions of recorded talks and lectures.
Each edition fills the gaps in what the speaker says, checks claims against
sources, adds precise dates, footnotes, links, pictures and drawings.
Languages: **English and French**. Every page exists in both (see "Two languages" below).

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
works/<slug>/index.qmd       one folder per work (English)
works/<slug>/images/         images for that work, each with a credit (shared by both languages)
fr/                          the French site: same structure (fr/index.qmd, fr/about.qmd, fr/works/<slug>/index.qmd)
fr/_metadata.yml             French defaults (lang, table-of-contents title, labels)
tools/                       scripts that generate drawings (e.g. timelines, in EN and FR)
.github/workflows/           publish.yml (build + deploy), check-links.yml (weekly link check)
```

## Adding a new work

1. Create `works/<short-slug>/index.qmd` (lowercase, hyphens) and its French twin
   `fr/works/<short-slug>/index.qmd`.
2. Add an entry to the `<ul class="sr-library">` list in `index.qmd` and in `fr/index.qmd`.
3. Front matter: `title`, `subtitle` (speaker, date, what the edition is), `date-modified: last-modified`.
4. While unfinished, start the page with a `::: {.sr-status}` line saying what is done.
5. A multi-chapter work (a lecture series) gets one folder with one `.qmd` per chapter
   and an `index.qmd` table of contents.

## Writing conventions

**Tone.** Clear, scholarly, never stiff, and humble. The edition reports what the
sources say; it does not lecture the speaker or the reader. Prefer "may understate"
to "is wrong", "it is perhaps worth noting" to "the irony is obvious". Personal
remarks are welcome when they add something (a judgement, a connection), but
phrased as the edition's judgement, not as invented personal experience: never
"I was surprised to find".

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

**Inline links** are for explanations: a link on the name of an event, person,
organisation, text or concept, to a page that explains it to a curious reader.
Link the **first mention** only. See "Choosing link targets" below.

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
general overviews. Footnotes **prove**: they point to the most authoritative source,
even a book. When sources disagree, the note says so and names them.

## Choosing link targets

A link **explains**: it points to the best free explanation a curious reader can
read in a few minutes.

| What is linked | First choice | Then |
|---|---|---|
| Philosopher or concept | *Stanford Encyclopedia of Philosophy* | *Internet Encyclopedia of Philosophy*, Britannica |
| Other person | Page of an institution tied to them (Nobel Prize, Collège de France, Institut Pasteur…) | Britannica, Wikipedia |
| Event | A university or archive teaching project (e.g. *Seventeen Moments in Soviet History*) | Britannica, Wikipedia |
| Text or book | The text itself if legally free (Gallica/BnF, archive.org, university sourcebooks) | Scholarly or institutional page about it, Britannica |
| Organisation or journal | Its own archive or an institutional page | Britannica, Wikipedia |

Rules:

- Every target must be written or edited by people with expertise, free to read
  (no paywall: no Universalis), stable, and explanatory rather than opinionated.
  Avoid blogs, SEO sites, AI-generated aggregators, and partisan sites (unless the
  partisan site is itself the primary source).
- **Wikipedia only when nothing on a better line of the table exists** for that item.
- **Accuracy beats rank:** if a higher-ranked page is wrong on the point at hand,
  use the next one (and say so in a note if it matters).
- When the best page is in another language, add "(in French)" / "(en anglais)".
- **Open every URL before using it** and check that it says what we claim.
  The weekly link check (`check-links.yml`) reports links that break later by
  opening an issue on GitHub.

## Two languages

- English pages live at `/…`, French pages at `/fr/…`, with **the same path** after `/fr`.
- The EN | FR switch in the navigation bar takes the reader to **the same place**
  in the other language. It relies on two rules, which every edit must respect:
  1. **Same heading ids** in both versions: give every `##` and `###` an explicit id,
     identical in both files (`## I. Les derniers staliniens {#sec-stalinists}`).
  2. **Same sequence of blocks** under each heading: the same number and order of
     paragraphs, quotes, lists, figures, boxes and timestamps. Translate block by
     block; never merge or split paragraphs in only one language.
- In French, the speaker's words are translated by the edition, with the original
  inside the quote:

```markdown
> Traduction française.
>
> <details class="sr-original"><summary>Texte original</summary>Original English words.</details>
```

- French links point to French-language sources of equal quality when they exist
  (Larousse, BnF, French Wikipedia under the same rule as above); the targets can
  therefore differ between the two versions. Notes cite French editions of books
  when they exist.
- Workflow: write and agree the English section first, then translate it.
  Every later correction is made in both files.

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
