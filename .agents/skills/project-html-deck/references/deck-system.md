# Deck system

## Communication job

Before coding, write one private sentence:

> By the end, [audience] should [understand or do something] because [central takeaway].

Do not place this sentence on a slide.

## Default four-slide weekly report

1. **Outcome** — the week's one-sentence result and strongest relevant image
2. **Metrics** — two to four before/after numbers with their comparison basis
3. **Issue and response** — what happened, what was done, and what is still being monitored
4. **Next week** — no more than three actions, each specific enough to verify

Change the slide count when the user requests it or the evidence cannot support this structure.

## Composition rules

- Use one composition per slide rather than a collection of small cards.
- Keep equal outer margins and a consistent top rule, section marker, and page number.
- Use asymmetry deliberately: large type on one side and one dominant visual on the other.
- Crop screenshots to the exact area the presenter needs to discuss. Do not shrink a full desktop screenshot until its labels are unreadable.
- Keep external service logos in their official colors; keep the rest of the palette restrained.
- Do not invent charts when there are fewer than two comparable values.

## Interaction rules

- Use CSS transitions or keyframes for sequential reveal, number emphasis, underline drawing, and restrained image movement.
- Avoid perpetual motion and gratuitous bouncing.
- Respect `prefers-reduced-motion`.
- Print styles must disable animation and show the final state.

## Required QA evidence

`scripts/export_deck.py` creates:

- the PDF
- one PNG per page
- `contact-sheet.png`
- `report.json` with page count

Completion requires visual inspection of every page, not merely successful command exit.
