"""Check the generated export without writing to a Vikunja server."""
import json
import re
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
folder = root / 'exports' / 'vikunja'
projects = json.loads((folder / 'data.json').read_text(encoding='utf-8'))
assert len(projects) == 1
project = projects[0]
tasks = project['tasks']
assert len(tasks) == 62
seen = set()
relations = {'parenttask': 0, 'blocked': 0}
epics = stories = 0
sprints = set()
keys = set()
for task in tasks:
    assert task['id'] not in seen
    assert task['done'] is False and task['bucket_id'] == 1
    assert not task['assignees']
    assert not any(key in task for key in ('start_date', 'end_date', 'due_date'))
    key = re.match(r'\[(CAL-(?:E\d{2}|\d{3}))\]', task['title'])[1]
    assert key not in keys
    keys.add(key)
    for kind, targets in task['related_tasks'].items():
        assert len({target['id'] for target in targets}) == len(targets)
        for target in targets:
            assert target['id'] in seen, (key, kind, target)
            relations[kind] += 1
    seen.add(task['id'])
    labels = {label['title'] for label in task['labels']}
    epics += 'type:epic' in labels
    stories += 'type:story' in labels
    sprints.update(label for label in labels if label.startswith('sprint:'))
    if 'type:story' in labels:
        assert len(task['related_tasks']['parenttask']) == 1
        for field in ('Completed outcome:', 'Acceptance checklist:',
                      'Documentation deliverables:', 'Runbook decisions to record:'):
            assert field in task['description'], (key, field)
        assert '<strong>' in task['description']
assert (epics, stories) == (12, 50)
assert relations == {'parenttask': 50, 'blocked': 95}
assert len(sprints) == 8
plan = (root / 'plan.md').read_text(encoding='utf-8-sig')
plan_keys = set(re.findall(r'^### (CAL-\d{3})', plan, re.M))
assert plan_keys == {key for key in keys if not key.startswith('CAL-E')}
assert len(project['views']) == 3 and len(project['buckets']) == 6
board = next(view for view in project['views'] if view['view_kind'] == 'kanban')
assert board['bucket_configuration_mode'] == 'manual'
assert board['default_bucket_id'] == 1 and board['done_bucket_id'] == 5
assert len(project['task_buckets']) == 62
assert {entry['task_id'] for entry in project['task_buckets']} == seen
with zipfile.ZipFile(folder / 'calicortado-vikunja-import.zip') as archive:
    assert set(archive.namelist()) == {'data.json', 'VERSION'}
    assert archive.read('data.json') == (folder / 'data.json').read_bytes()
    assert archive.read('VERSION') == b'v2.6.0'
    assert archive.testzip() is None
print(json.dumps({'result': 'PASS', 'epics': epics, 'stories': stories,
                  'relations': relations, 'sprints': len(sprints),
                  'views': 3, 'buckets': 6, 'live_import_tested': False}, indent=2))
