# Calicortado

Calicortado is a personal second brain: capture thoughts quickly, keep notes in plain Markdown, and retrieve useful information through search and local AI answers.

Status: E01 foundation completed locally, 2026-09-27. Product scope, environment inventory, offline tooling and seven API contracts are documented and checked. This is not a running product. E01 completion is synchronized to Vikunja; CAL-005 is In progress. The source baseline is published; no services have been deployed. See [E01 evidence](docs/acceptance/e01.md).

## First complete release

Confirmed baseline: Obsidian is the offline editor on iPhone and Mac. Calicortado adds encrypted sync, reliable capture, tested recovery, private remote access, direct search, cited local AI answers and a responsive web display. The user handles device setup. [Release scope](docs/release-scope.md) distinguishes confirmed choices from proposed targets.

The layers are independently deployable. Data, embeddings/retrieval, inference and display communicate through their own domain addresses behind Traefik. They can initially share suitable hosts, but release acceptance includes an actual separate-machine deployment and layer relocation test.

Default domain addresses derive from the `DOMAIN` environment variable, set by the deployment environment, with independent per-service URL overrides. Follow [development and configuration](docs/development.md) to run the offline checks or render another environment's addresses.

## Start here

New to the project? Read the [plain-language proposal](docs/proposal.md), or open the [illustrated HTML reading copy](docs/proposal.html). It explains the user experience, full architecture, technology, privacy boundaries and delivery stages. The [overview diagram](docs/architecture-overview.svg) and [service-flow diagram](docs/architecture-flow.svg) can also be viewed separately.

[plan.md](plan.md) is the detailed **Vikunja-shaped backlog: 12 component epics, 50 stories, eight proposed sprints**. Every story has a completed outcome, blockers, steps, acceptance checks, documentation deliverables and required runbook decisions. The generated [Vikunja import ZIP](exports/vikunja/calicortado-vikunja-import.zip) and [JSON](exports/vikunja/data.json) are now available; follow the [import guide](exports/vikunja/README.md). The user-imported board is now verified (62 tasks); E01 completion and CAL-005 pickup are synchronized.

| Document | Purpose |
|---|---|
| [Sprint plan and backlog](plan.md) | Ordered delivery goals and individually pickable stories |
| [Architecture](projects/second-brain.md) | Layer ownership, domain register, API contracts and trust boundaries |
| [Design](design.md) | Capture experience, offline behavior, privacy and phone storage |
| [Recovery](projects/recoverability.md) | Calicortado backup sources, independent repository and restore |
| [Remote access](projects/remote-access.md) | Private user routes and device behavior |
| [Map](map.md) | Component relationships, epic ownership and next work |
| [Runbook](runbook.md) | Every decision, rationale, status, consequences and evidence |
| [Working agreement](AGENTS.md) | Documentation and implementation rules |

Documentation is part of each story's Definition of Done, not a final cleanup task. Every decision must be logged in the runbook as it is made.

## Implementation boundary

This directory owns product planning and future application code. Deployment configuration belongs in the separate infrastructure repository, using its Git workflow. Links run from here to infrastructure; infrastructure documents must not mention Calicortado.

Notes, secrets and private exports stay outside source control. Planning does not grant deployment, account, remote-creation or publication permission.

## Next action

CAL-005 is in progress: the [domain registry and verification procedure](docs/operations/endpoints.md) are prepared using `${DOMAIN}`. Private resolver/ingress inputs are recorded; selected live DNS/router configurations show no candidate-prefix collision. A disposable local HTTPS/authentication rehearsal passed seven checks and was cleaned up. The infrastructure checkout now matches its remote, and the two-phase live probe/DNS change and rollback are prepared. Live activation awaits the requested authorization and operator-owned sudo steps. Live mutations follow the [access matrix](docs/operations/access.md); E01 does not authorize deployment. The iPhone capture trial follows the sync prototype.
