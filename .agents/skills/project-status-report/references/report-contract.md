# Report contract

## Evidence precedence

1. The user's latest explicit correction
2. A human-approved fact in `PROJECT_STATE.md`
3. A later dated source record that explicitly changes an earlier decision
4. Earlier source records

Do not overwrite a conflict silently. Show both claims, their filenames, and the person or action needed to resolve them.

## Daily Slack draft

```text
[오늘 한 일] YYYY.MM.DD

프로젝트: [project]

✅ 완료
- [observable completed work] ([evidence filename])

🔄 진행
- [current work and the next observable checkpoint] ([evidence filename])

⚠️ 확인 필요
- [question, risk, or human decision required] ([evidence filename])
```

Omit an empty section. Keep a single fact in one bullet unless separating it changes the status meaning.

## Weekly report source outline

Use this order when the report will feed a deck or video:

1. This week's outcome in one sentence
2. Two to four confirmed metrics with before/after context
3. Completed work
4. Issue and response, clearly separating deployment from monitoring
5. Next week's actions
6. Evidence index

## Quality checks

- No future folders were used.
- Every metric matches its source.
- Proposed, approved, deployed, and verified are not treated as synonyms.
- AI-written drafts are not described as fully automatic customer responses when a person reviews them.
- No private names, phone numbers, addresses, credentials, or tokens appear in an external-facing draft.
