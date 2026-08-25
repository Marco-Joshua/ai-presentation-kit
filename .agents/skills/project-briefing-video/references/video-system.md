# Video system

## Manifest fields

Top level:

```json
{
  "meta": {"brand": "...", "period": "...", "accent": "#245BFF"},
  "voice": {"id": "F2", "speed": 1.08, "steps": 8},
  "bgm": "optional/path.mp3",
  "bgmVolume": 0.07,
  "scenes": []
}
```

Every scene requires `type`, `title`, and `narration`. Use `closedCaption` for a concise narration caption and `caption` for the persistent footer summary. Use `image` only when the file exists and strengthens the current claim.

Supported scene types:

- `hero` — opening claim and a dominant image
- `sources` — evidence channels or inputs
- `metrics` — two to four before/after numbers
- `list` — completed work, decisions, or next actions
- `compare` — conflict, before/after, or issue/response
- `closing` — conclusion and next step

## Storyboard rules

- One scene, one spoken claim.
- The first three seconds must establish the topic and why it matters.
- Use metrics only with a clear comparison basis.
- Keep each narration sentence short enough to match one visual beat.
- Use scene-level captions that remain readable in a YouTube player; do not paste the whole narration into a tiny box.
- A report video should sound like a report. Remove comments about how long production took or which lesson is being demonstrated.

## Motion vocabulary

Choose only what supports the claim:

- spring entrance for the main title or image
- count-up for a confirmed metric
- line reveal for comparison or progress
- masked crop or subtle camera move for a screenshot
- sequential reveal for two or three actions

Do not animate every element, loop decorative movement, or use generic floating cards.

## QA

The renderer must produce `output/qa/<video-name>/` containing:

- start, middle, and end frames
- one representative frame per scene
- a contact sheet
- `probe.json`

Open and inspect these files. Command success alone is not visual QA.
