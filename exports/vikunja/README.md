# Import Calicortado into Vikunja

Generated for Vikunja **v2.6.0**, observed from the supplied instance's public info endpoint on 2026-09-27. Its `vikunja-file` importer is enabled.

## File to upload

Use [calicortado-vikunja-import.zip](calicortado-vikunja-import.zip), not the bare JSON.

1. Sign in to your Vikunja instance.
2. Open **Settings → Import** and select **Vikunja export**.
3. Upload the ZIP and complete the import.
4. Open the new **Calicortado** project and check the List, Board and Table views.

The native importer expects `data.json` and `VERSION` at the ZIP root. The readable JSON is also provided as [data.json](data.json). See the [official import instructions](https://vikunja.io/help/import-and-export/).

## Expected result

- One Calicortado project; 12 epic tasks and 50 story tasks.
- 50 story-to-parent relations and 95 blocked-by dependencies. Vikunja creates inverse relations automatically.
- Sprint, component, release, task-type and estimate labels.
- Full HTML-formatted story descriptions, acceptance checklists, documentation requirements and decision-log requirements.
- Backlog, Ready, In progress, Review, Done and Blocked columns; every task initially in Backlog and not done.
- No assignees, deadlines, reminders, credentials or private notes.

The plan's “Normal” priority maps to Vikunja Medium (2); High maps to 3. Planning IDs such as CAL-001 remain in titles. Numbers in [task-id-map.json](task-id-map.json) are archive-local IDs, not the IDs your server will assign.

This import creates a new project; it is not a merge/update operation. Import once. If an attempt reports an error, inspect whether a project was created before retrying to avoid duplicates.

Repository-document references in descriptions remain named references because these documents are not published at web URLs. They are not broken links into the Vikunja website.

## Verification and limits

Checked the official v2.6.0 importer/model source, archive structure, JSON types used by the exporter, IDs, backward-only relation ordering, counts, labels and view/bucket mapping. All 50 stories carry their required detail. No authenticated import was performed, so server-side acceptance and final editor rendering remain to be checked after upload.

Relations refer only to previously emitted tasks: this avoids v2.6.0 eagerly creating a forward-reference target as an extra task. Epics are emitted first, followed by a topological ordering of stories. Only one direction of each relation is supplied.

## Regenerate

From the project root with PowerShell 7:

```powershell
./tools/export-vikunja.ps1
python ./tools/validate-vikunja.py
```

The exporter reads plan.md and performs no network calls. The ZIP is a generated artifact; it is not a second manually maintained backlog.

Source references: [file importer](https://github.com/go-vikunja/vikunja/blob/v2.6.0/pkg/modules/migration/vikunja-file/vikunja.go), [structure importer](https://github.com/go-vikunja/vikunja/blob/v2.6.0/pkg/modules/migration/create_from_structure.go), [project model](https://github.com/go-vikunja/vikunja/blob/v2.6.0/pkg/models/project.go), [view model](https://github.com/go-vikunja/vikunja/blob/v2.6.0/pkg/models/project_view.go).

## Snapshot status after E01

The supplied ZIP/JSON is the sanitized 2026-09-27 all-Backlog import snapshot. E01 completion is recorded in [the plan](../../plan.md) and [evidence](../../docs/acceptance/e01.md); no live tasks were updated. Do not re-import to synchronize progress: record server IDs and update the existing tasks after the initial import. The exporter currently creates an initial backlog, not an execution-state synchronization package.

Identifying deployment names were removed from both JSON and ZIP. Task IDs, statuses and dependency relations were preserved; this sanitization is not a live board update.
