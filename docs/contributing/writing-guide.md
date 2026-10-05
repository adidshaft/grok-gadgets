# Writing guide

Use concise technical English inspired by [ASD-STE100](https://www.asd-ste100.org/STE_faq.html). The standard includes writing rules and a controlled dictionary. This project does not claim formal compliance. The rules below are our project guidance, not a replacement for the standard.

## Help the reader complete one task

- State what the component does in the first paragraph.
- Use short sentences, active verbs and consistent terms.
- Define an acronym on first use. Keep exact code and API names.
- Put one action in each numbered step. Give the expected result.
- Use a diagram for connections and a table for choices or support levels.
- Explain each diagram in text. Label planned or unverified paths.
- Link to one canonical explanation instead of copying it into several pages.
- Keep build history and audit evidence outside the getting-started flow.
- State what works now and link to remaining work. Avoid repeated disclaimers.

## Keep each surface focused

| Surface | Content |
| --- | --- |
| README | Purpose, current support, one starting path, diagram and contribution links |
| Website | What users can do, short examples, honest status and links to detailed docs |
| Task guide | Requirements, steps, expected result and recovery |
| Reference | API details, protocol rules and board configuration |
| Issue | Problem, evidence, acceptance criteria and dependencies |
| Pull request | User-visible change, linked issue, validation and limitations |

Use “reusable ESP32 library; C124 example” instead of implying that the SDK supports only one board. Do not replace that claim with “works on every ESP32.” Supported boards need evidence.

Before review, remove repeated background, verify commands and links, and check that a beginner can identify the next step. This guide applies to all five repositories and public project copy.
