# Calicortado design

Status: product scope confirmed, updated 2026-09-27; timing/storage targets remain proposals. The first complete release includes direct search and local AI answers; their implementation order is in the component stories in [plan.md](plan.md). The user owns iPhone/Mac setup and device observations. See [release baseline](docs/release-scope.md).

## Outcome and users

Capture a thought in seconds on the iPhone or Mac, find it later without remembering where it was filed, and ask questions that return the source notes. The user-confirmed baseline keeps Obsidian for offline editing and adds a Calicortado web display for capture, search and answers.

The user is the first participant. Additional users may join later through explicitly shared or separate private vaults. Secondary Android devices and the Windows workstation are optional clients, not MVP requirements.

## Experience

1. One inbox; no required title, folder or tag choice during capture.
2. Plain Markdown notes remain readable and editable offline.
3. Skipped days create no catch-up requirement. No streaks or escalating reminders.
4. Search and capture remain useful when AI is unavailable.
5. Show conflicts and failures, preserve the captured text, and offer a manual path.
6. Add components only when they remove demonstrated friction.

Capture should take under 10 seconds in the trial. Local search is the first retrieval interface. Remote search later returns snippets and source links directly, without requiring a model to select a tool.

## Ownership and privacy

Notes stay on user devices and selected private infrastructure. Cloud inference on note content is outside the plan. Passwords stay in the password manager.

Use separate vaults for personal and shared material. Another user's private vault is not bridged or indexed without explicit opt-in. Search authorization must enforce vault boundaries independently of the model.

The proposed bridge holds the encryption passphrase and produces plaintext inside the data component. Sync encryption does not conceal those notes from the data host. Confirm this trust boundary before real data is added. Other layers use authorized domain APIs rather than mounting the mirror.

## Storage on the iPhone

Target phones have limited local storage. The proposed budget for Obsidian vault files and its sync database is 500 MB, to measure during setup and after 30 days.

Keep photos in Immich, documents in Paperless, bookmarks in Karakeep and long recordings in their source app; link to them from notes. Keep text notes, including archives, offline by default. Test attachment filters before relying on them. Excluding archives or making the phone capture-only would change the offline promise and needs an explicit choice.

Do not promise particular sync overhead, background behavior or on-demand fetching until measured on the selected versions.

## Automation contract

| Feature | Permitted effect | Pause and failure behavior |
|---|---|---|
| Capture Shortcut | Create a new inbox note | Preserve text if capture fails; allow local capture offline |
| Later capture webhook | Create once in the owner's inbox; never overwrite | Revoke device token or disable workflow; retry uses the same request identity |
| Optional digest and resurfacing | Write generated material only into `_ai/`, with source links | Explicit enable/disable; label stale results; no repeated failure messages |
| Optional archive | Move eligible notes only under an explicitly enabled rule; never rewrite or delete | Log reversible moves; respect `archive: never`; remain paused until explicitly resumed |

Human text is never rewritten by AI. Create-only capture and an explicitly enabled archive are the only proposed exceptions to automation writing exclusively in `_ai/`. Auto-archive is deferred until ordinary capture and retrieval work well.

Routine success stays quiet. Notifications identify an actionable failure or a user-selected review. Review timing is unset.

## Validate through use

Trial capture for 14 days, starting in CAL-017. The proposed release gate is useful captures on at least 10 days, assessed from timestamps without daily scoring. Synthetic-data implementation can continue while observations accumulate; failed usability or recovery gates block release or real-data expansion until resolved. Skipped days never prevent use. CAL-049 records actual trial and day-30 storage evidence or an explicitly agreed revision of the gate.

Keep, simplify or remove features according to effort saved, predictability and maintenance.
