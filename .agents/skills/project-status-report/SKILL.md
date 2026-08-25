---
name: project-status-report
description: Create evidence-grounded daily reports, weekly reports, Slack updates, and project status briefs from refs/YYYYMMDD and PROJECT_STATE.md. Use for requests such as 오늘 한 일, 일일보고, 주간보고, 업무 브리핑, or status summary; do not use it as the final slide or video production workflow.
---

# Project Status Report

Turn project records into a report that a person can review and send without inventing work.

## Required workflow

1. Resolve the repository root and current system date before selecting evidence.
2. Treat the user's latest request as authoritative for date range, audience, length, and format.
3. Read `PROJECT_STATE.md` plus the selected `refs/YYYYMMDD/` files. Preserve source files unchanged.
4. Use Git changes only as supporting evidence. Do not report edits to this kit's instructions, skills, templates, or generated output as business accomplishments unless a source record explicitly says they are project work.
5. Separate `완료`, `진행`, and `확인 필요`. A deployed change that still needs observation belongs in both `완료: 배포` and `진행: 모니터링` rather than being flattened into one status.
6. Put the evidence filename at the end of each substantive bullet. Use only numbers, dates, owners, and outcomes found in evidence.
7. Show a review draft. Never send to Slack, email, or another external destination without explicit approval.

## Date selection

- `오늘`, `오늘 한 일`, and `일일보고`: use only the folder matching the current system date, `refs/YYYYMMDD/`. If it does not exist, report that exact missing path and stop instead of silently substituting another day.
- `주간보고`: use the Monday of the current week through the current date, inclusive.
- Explicit dates override these defaults, including a rehearsal request that names a prepared future example date.
- For relative requests such as `오늘` or `이번 주`, never read a future-dated folder into the result.

## Output

- For chat-only requests, show the draft directly.
- When a file is requested, save it under `output/` with the resolved date in the filename.
- Keep Slack drafts compact enough to scan on one screen; keep evidence filenames but omit implementation chatter.

Read [references/report-contract.md](references/report-contract.md) when producing the final report format or resolving conflicting records.
