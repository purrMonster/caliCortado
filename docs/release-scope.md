# Release baseline — CAL-001

Recorded 2026-09-27. The user confirmed Obsidian on iPhone/Mac plus the Calicortado capture, search and local AI answers display. The user owns device installation/setup and supplies human trial evidence. The chosen environment value is the environment-configured DOMAIN; domain names must remain configurable with independent service URL overrides. See [decisions and handoff](../runbook.md) and [release gates](../plan.md#release-definition).

## Included outcomes

- Capture to one inbox from iPhone, Mac and the web; preserve text offline and retry without duplication.
- Edit ordinary Markdown offline in Obsidian; encrypted self-hosted sync and visible conflict handling.
- Restore notes and required service state from an independent backup.
- Reach authorized services privately away from home.
- Search current authorized sources without depending on inference availability.
- Ask for local AI answers with citations, explicit insufficient evidence and bounded outages.
- Deploy data, compute, inference and display independently through configurable HTTPS domain interfaces behind Traefik; prove separation and relocation at release.

Shared household rollout, a custom native editor, cloud inference, autonomous write/action agents, automatic archive/digests, bulk imports and external content integrations are deferred. Synthetic notes only until recovery/onboarding gates pass. A plaintext bridge in the data component is an explicit trust boundary; confirm its real-data use during CAL-009/CAL-017.

## Targets and owners

| Outcome | Status and target | Evidence owner / gate |
|---|---|---|
| Capture | Proposed under 10 seconds, no mandatory filing | User device test, CAL-014/CAL-015 |
| Foreground sync | Proposed within 60 seconds; no background iOS promise | User on devices with implementation evidence, CAL-009 |
| Index freshness | Proposed within five minutes while healthy | Implementer, CAL-032 |
| Recovery point/time and retention | Unset; obtain owner choice before backup rollout | User, CAL-018/CAL-020 |
| AI latency/availability | Unset until hardware benchmark; no automatic wake or cloud fallback | User accepts measurements, CAL-034 |
| Phone storage | Proposed 500 MB vault plus sync database | User initial and day-30 measurements, CAL-049 |
| Daily use | Proposed 14-day trial with useful capture on 10 days | User, CAL-017/CAL-049 |
| Backup observation | Seven actual daily observations | Implementer, CAL-021 |

These targets were retained from the plan, not silently approved by confirming the product shape. Device setup ownership is confirmed; device setup itself is not complete. Deployment, restarts, spending, downtime and real-data imports remain unapproved in the [access matrix](operations/access.md). Missing production inputs do not block offline development.
