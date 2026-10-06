# student-judge competency report — draft

**Judged at:** 2026-10-04T22:48:00-04:00
**Evidence pass:** current Phase 5 native chat + current docs/report.md, docs/diagrams/, and docs/wireframes/; prior judge.md ignored. Other project chats were listed but their message contents were not available in this pass, so this is provisional.

**Student / session:** COMP 3613 Student Accommodation project; Copilot Agent workspace chats
**Artifact:** Accessible Phase 5 Guide chat, project report, use-case diagram, model diagram, and wireframe
**Phases in evidence:** 1–5 (COMP 3613; Phase 5 polish; Phase 6 deploy not started)

### Totals
| | Count / value |
|--|--|
| Metrics on rubric | 12 (M1–M12) |
| N/A (excluded) | 0 |
| Metrics scored | 12 |
| Scoreable max | 12 × 4 |
| Awarded total | 37 / 48 |
| **Overall (avg of scored)** | **3.1 / 4** |
| Impression mark | 15 / 20 (estimated from overall; no Guide confidence log found) |

## Scorecard

| ID | Metric | Score / 4 | In avg | Evidence |
|----|--------|----------:|:------:|----------|
| M1 | Phase discipline | 3 | yes | The report has the use-case, ERD, and wireframe before the Phase 5 implementation notes. The current work remains in Phase 5; no premature deployment is recorded. |
| M2 | Problem framing | 3 | yes | The report names the Student Accommodation project and three workflows, then records the actors, relationships, fields, and theming choices. Accessible Phase 5 messages continue from those named features rather than introducing a different product. |
| M3 | Decision ownership | 3 | yes | The student steered visible product decisions: “do the listings on the home tab, get rid of the images” and later asked for a separate My Home and landlord controls. |
| M4 | Artefact-before-code | 3 | yes | The report contains an ERD and wireframe coverage notes; implementation follows the listing, booking, landlord, and review concepts in those artefacts. |
| M5 | Verification habit | 3 | yes | The student reported observable results and mismatches, including “log in works,” a blank Home screen, a PowerShell bind error, and “when i click view stay and review it says internal server error.” The latest review fix has not yet received a student confirmation. |
| M6 | Assignment fit | 3 | yes | The report records thin routes, services, repositories, and model snippets for the implemented workflows. No student route snippet with inline SQL is recorded. |
| M7 | Slice explanation | 3 | yes | The student completed model, repository, service, and thin-route checks recorded in `docs/report.md`; the Add Listing route was corrected to pass `user.id` rather than a User object. |
| M8 | Prompt quality | 3 | yes | Requests are concrete and tied to actual app behavior, for example “make the listings color white, font black” and the reported My Home server error. |
| M9 | Response to pushback | 3 | yes | The student continued to report and steer changes after the initial listing page, including moving listings to Home, hiding images, adding My Home/reviews, and reporting the review error after testing it. |
| M10 | Integrity | 3 | yes | No paste-back, external-assist, transcript-editing, or skill-editing signal appears in the accessible Phase 5 chat or current report. This is limited by unavailable older chat contents. |
| M11 | Provenance continuity | 3 | yes | The accessible implementation requests and error reports correspond to the project’s existing workflows, local routes, and database schema. |
| M12 | Sincerity trajectory | 4 | yes | No suspicion protocol was needed in the accessible evidence. The student’s follow-up “when i click view stay and review it says internal server error” provides a specific, project-grounded report rather than a pasted solution. |

## Strengths
- The project has the required three named workflows, a use-case diagram, an ERD, and a wireframe with coverage recorded in the report.
- Phase 5 decisions are iterative and specific: home-page listings, card styling, landlord management, and a separate tenant My Home/review flow.
- The student gave actionable observations from running the app, including login success and specific failures, then continued steering the implementation.
- The report records student code-check attempts across the model, repository, service, and thin-route layers.

## Gaps (priority order)
1. **Phase 5 polish is still in progress.** The latest schema fix returned HTTP 200 in an agent-side check, but the student has not yet confirmed it in their browser. The new request to remove/cancel a My Home stay is also not implemented yet.
2. **Phase 6 has not started.** No deployed URL or marker logins are recorded; deployment should follow completion of local polish.
3. **Evidence limitation:** older Phase 1–4 native chat contents were unavailable during this draft. Their artefacts are present, but a fresh assessment of those turns could adjust M2, M3, M8, M10, or M11.

## Phase gate status
| Phase | Status | Note |
|-------|--------|------|
| 1 | met | Assigned project and three workflows are in the report. |
| 2 | met | Use-case PNG exists and is embedded; includes and actor associations are summarized. |
| 3 | met | ERD and relationship notes are in the report. |
| 4 | met | Wireframe is embedded and all three named workflows have coverage blocks. |
| 5 | partial | Theme and workflows are implemented with substantial student steering and code checks. Some browser verification remains pending after fixes; the latest requested cancellation/remove action has not yet been built. |
| 6 | not met | No deployment evidence; appropriately pending Phase 5 polish. |

## Recommended next practice
- Finish the My Home cancellation flow, then run the app locally and report whether cancelling the stay removes it from My Home while preserving the listing and review history as intended.

## Integrity note
- Clean within available evidence; no external-assist or paste-back concern identified.

## Provenance flags
- None identified in the accessible Phase 5 chat. Older phase chats were not readable in this assessment pass.

## Sincerity log summary
- Blocks found: 0 | max round: none | min/mean/final confidence: N/A | trend: N/A | cleared: N/A (no suspicion round was needed in the accessible chat)

## Skips
- Skips: 1/3 used
- Listing model field declarations — assumed: declare the ERD/wireframe listing fields plus the requested image URL.

**Draft note:** This is a preliminary assessment because the older native Guide chats could not be read. Reassess before report export or final submission.
