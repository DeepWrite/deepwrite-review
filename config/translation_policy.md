# Translation Policy

English and Korean editions are parallel publications, not rough mirrors. Each edition must be editorially coherent in its own language.

## Requirements

- Preserve thesis, argument structure, evidence, citations, uncertainty, and qualifications.
- Preserve footnotes and bibliography entries.
- Use stable counterpart links.
- Flag any concept that cannot be translated without loss.
- Do not simplify one language version unless the other version is revised accordingly.

## Two-Dimensional Review Standard

Content fidelity is necessary but not sufficient. A translation that correctly reflects the English argument but reads as 번역투 (translation-ese) has not passed review.

Translation review must assess two dimensions independently:

**1. Content fidelity** — Does the Korean version accurately preserve the thesis, evidence, argument structure, citations, uncertainty markers, and qualifications of the English original?

**2. Prose quality** — Does the Korean version read as independent Korean intellectual journalism? Would a reader encountering the Korean version alone find it natural, forceful, and coherent as a piece of Korean prose?

Both dimensions must pass before `translation_status: checked` can be recorded.

## Korean Prose Standard

The standard for Korean prose quality is defined in `config/style_guide_ko.md`. Editors performing translation review must apply that guide. The most common failure modes are:

- Mechanical calquing of English pronoun structures ("그것은…" for "It is…")
- Using "도착하다" for abstract phenomena instead of "달고 오다", "찾아오다", "나타나다"
- Translating "old-fashioned" as "낡은" when "구닥다리" or "구식의" is more precise
- Carrying English compound modifier structures into Korean without restructuring
- Direct borrowing of English section-heading conventions ("노트" for "Note")
- Titles that read as newspaper headlines rather than magazine headings

## Untranslatable Concepts

When a political or institutional concept carries significant connotation in English that cannot be fully carried into Korean without distortion, use the following approach:

1. Provide the Korean equivalent as the primary term.
2. Include the English original in parentheses on first use: 민주주의의 후퇴(democratic backsliding).
3. Do not adopt the English term as a loanword unless it is already established in Korean usage.

## Status

Translations must not be published until both `translation_status: checked` and Chief Editor approval are recorded. "Checked" requires passing both the content fidelity review and the Korean prose quality review as specified above.
