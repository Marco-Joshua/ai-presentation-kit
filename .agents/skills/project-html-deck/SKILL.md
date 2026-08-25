---
name: project-html-deck
description: Create and verify presentation-style 16:9 HTML decks and PDFs from project reports or refs. Use for 발표자료, PPT, 피피티, 장표, deck, or PDF requests where this repository's interactive editorial visual system should be preserved.
---

# Project HTML Deck

Build an audience-facing deck, not a document split across slides.

## Scope

- In this kit, an ordinary `PPT` or `피피티` request means paginated 16:9 HTML plus PDF so the screen version can keep motion. Create a `.pptx` only when the user explicitly asks for that file format.
- Use an approved report when one exists. Otherwise apply the evidence rules in `$project-status-report` before designing.
- The user's latest request controls audience, purpose, slide count, tone, and output format.

## Required workflow

1. Read `장표_템플릿.html`, the relevant source report or selected `refs` records, and inventory usable files in `refs/**/첨부/` and `assets/visuals/`.
2. Plan one claim per slide. Prefer a short arc such as outcome → evidence → issue/action → next step.
3. Reuse real screenshots and supplied images first. If a relevant image exists, make at least one slide use it as a dominant visual instead of producing an all-text deck. If Codex image generation is available and a needed visual is missing, generate a correctly framed asset and inspect it before use.
4. Create a self-contained HTML deck in `output/`. Keep each `.slide` at 1920×1080 and make print CSS produce exactly one PDF page per slide.
5. Apply motion only to the screen version. The print/PDF state must show all essential information without relying on animation.
6. Run `python3 scripts/export_deck.py output/<name>.html --pdf output/<name>.pdf`.
7. Open every rendered QA page and the contact sheet. Fix clipping, overlap, tiny copy, broken images, weak contrast, and repetitive layout before reporting completion.

## Non-negotiable visual constraints

- White or near-white canvas, black editorial typography, and one accent color unless the user specifies a brand system.
- Title 70px or larger; body 26px or larger at the 1920×1080 design size.
- Real screenshots and meaningful images should be large enough to read on a shared screen.
- Avoid card grids, rounded UI tiles, decorative gradients, placeholder diagrams, tiny dashboards, and generic AI-looking illustrations.
- Numbers should be visual protagonists: count-up, reveal line, or a restrained before/after treatment.

Read [references/deck-system.md](references/deck-system.md) before authoring or revising the deck.

Use `examples/customer-support-weekly-20260827/` as the canonical quality bar for hierarchy, whitespace, large visual assets, and restrained motion. Never copy its business facts into another project.
