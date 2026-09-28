param([string]$OutputDirectory = 'exports/vikunja')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$plan = Get-Content -LiteralPath (Join-Path $root 'plan.md') -Raw
$output = Join-Path $root $OutputDirectory
New-Item -ItemType Directory -Path $output -Force | Out-Null

function Render-Description([string]$markdown) {
    # Repository-relative links are not valid inside a Vikunja description.
    $markdown = [regex]::Replace($markdown, '\[([^\]]+)\]\((?!https?://)([^)]+)\)', '$1 (repository document: $2)')
    return (ConvertFrom-Markdown -InputObject $markdown).Html
}
function Labels([string[]]$names) {
    return @($names | ForEach-Object { @{ title = $_; hex_color = '6b7280' } })
}
function New-Task([int]$id, [string]$title, [string]$description, [int]$priority, [string[]]$labels) {
    return [ordered]@{
        id=$id; title=$title; description=(Render-Description $description)
        project_id=1; done=$false; percent_done=0; priority=$priority
        labels=(Labels $labels); assignees=@(); related_tasks=@{}
        bucket_id=1; position=($id * 65536)
    }
}

$tasks = [System.Collections.Generic.List[object]]::new()
$idMap = @{}
$epicRows = [regex]::Matches($plan, '(?m)^\| \[(CAL-E\d{2})\] ([^|]+)\| `component:([^`]+)` \| ([^|]+)\| ([^|]+)\|\r?$')
if ($epicRows.Count -ne 12) { throw 'Expected 12 epic rows' }
$nextId = 1
foreach ($row in $epicRows) {
    $key=$row.Groups[1].Value; $title=$row.Groups[2].Value.Trim()
    $component=$row.Groups[3].Value; $outcome=$row.Groups[4].Value.Trim()
    $children=$row.Groups[5].Value.Trim()
    $description = @"
## Completed outcome
$outcome

## Child stories
$children

## Completion gate
Every child must meet its acceptance criteria. Review the component contract, domain/auth configuration, state ownership, setup, operating guide, failure diagnosis, upgrade/rollback and recovery instructions. Link dated evidence and exact revisions.

## Decision record
Log every decision in repository runbook.md as it is made, with story ID, date, context, alternatives, choice, reason, status, consequences and verification. Reference reused decisions explicitly. Documentation is part of Done.

## Scope
Calicortado v0.1: Obsidian-based capture/sync, recovery, private remote access, search, local AI answers and a separate display. Layers communicate through individual domain addresses behind Traefik. Repository plan.md and projects/second-brain.md own the full plan and architecture.
"@
    $task = New-Task $nextId "[$key] $title" $description 3 @('type:epic','release:v0.1',"component:$component")
    $tasks.Add($task); $idMap[$key]=$nextId; $nextId++
}
$cards = [regex]::Matches($plan, '(?ms)^### (CAL-\d{3}) — ([^\r\n]+)\r?\n(.*?)(?=^### CAL-\d{3}|^## CAL-E\d{2}|^## Release and remaining choices|\z)')
if ($cards.Count -ne 50) { throw 'Expected 50 stories' }
$pending = [System.Collections.Generic.List[object]]::new()
foreach ($card in $cards) {
    $key=$card.Groups[1].Value; $title=$card.Groups[2].Value; $body=$card.Groups[3].Value
    $parent=[regex]::Match($body,'\| Parent task \| (CAL-E\d{2})').Groups[1].Value
    $labelRow=[regex]::Match($body,'(?m)^\| Labels \| (.+) \|\r?$').Groups[1].Value
    $labelNames=@([regex]::Matches($labelRow,'`([^`]+)`') | ForEach-Object { $_.Groups[1].Value })
    $priorityName=[regex]::Match($body,'\| Priority \| ([^|]+)\|').Groups[1].Value.Trim()
    # The plan's Normal is represented by Vikunja's Medium (2); High is 3.
    $priority=if($priorityName -eq 'High'){3}else{2}
    $dependencyRow=[regex]::Match($body,'\| Blocked by \| ([^|]+)\|').Groups[1].Value
    $dependencies=@([regex]::Matches($dependencyRow,'CAL-\d{3}') | ForEach-Object { $_.Value })
    # Metadata remains in the description as well as native fields so each card stands alone.
    $body = $body -replace '\| Priority \| Normal \|','| Priority | Medium (plan: Normal) |'
    $pending.Add(@{key=$key;title=$title;body=$body;parent=$parent;labels=$labelNames;priority=$priority;deps=$dependencies})
}
# v2.6.0 creates forward relation targets eagerly. Emit only backward references.
while ($pending.Count) {
    $ready = @($pending | Where-Object { $item=$_; @($item.deps | Where-Object { -not $idMap.ContainsKey($_) }).Count -eq 0 })
    if (-not $ready.Count) { throw 'Cycle or missing blocker in plan' }
    foreach ($item in $ready) {
        $task=New-Task $nextId "[$($item.key)] $($item.title)" $item.body $item.priority $item.labels
        $task.related_tasks['parenttask']=@(@{id=$idMap[$item.parent]})
        if($item.deps.Count) { $task.related_tasks['blocked']=@($item.deps | ForEach-Object { @{id=$idMap[$_]} }) }
        $tasks.Add($task); $idMap[$item.key]=$nextId; $nextId++
        [void]$pending.Remove($item)
    }
}
$views=@(
    @{id=1;project_id=1;title='List';view_kind='list';position=100;bucket_configuration_mode='none'},
    @{id=2;project_id=1;title='Board';view_kind='kanban';position=200;bucket_configuration_mode='manual';default_bucket_id=1;done_bucket_id=5},
    @{id=3;project_id=1;title='Table';view_kind='table';position=300;bucket_configuration_mode='none'}
)
$bucketNames=@('Backlog','Ready','In progress','Review','Done','Blocked')
$buckets=@(for($i=0;$i -lt $bucketNames.Count;$i++) { @{id=($i+1);project_view_id=2;title=$bucketNames[$i];position=(($i+1)*65536);limit=0} })
$intro = ($plan -split '(?m)^## Pick-up instructions')[0]
$project=[ordered]@{
    id=1; title='Calicortado'; description=(Render-Description $intro)
    is_archived=$false; hex_color='795548'; tasks=@($tasks.ToArray()); views=$views; buckets=$buckets
    task_buckets=@($tasks | ForEach-Object { @{task_id=$_.id;project_view_id=2;bucket_id=1} })
    positions=@($tasks | ForEach-Object { @{task_id=$_.id;project_view_id=1;position=$_.position} })
    child_projects=@()
}
$json = ConvertTo-Json -InputObject @($project) -Depth 40
[IO.File]::WriteAllText((Join-Path $output 'data.json'),$json,[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $output 'VERSION'),'v2.6.0',[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $output 'task-id-map.json'),(ConvertTo-Json $idMap),[Text.UTF8Encoding]::new($false))
Add-Type -AssemblyName System.IO.Compression
$archivePath=Join-Path $output 'calicortado-vikunja-import.zip'
$stream=[IO.File]::Open($archivePath,[IO.FileMode]::Create)
$archive=[IO.Compression.ZipArchive]::new($stream,[IO.Compression.ZipArchiveMode]::Create)
try {
    foreach($name in @('data.json','VERSION')) {
        $entry=$archive.CreateEntry($name,[IO.Compression.CompressionLevel]::Optimal)
        $entryStream=$entry.Open()
        try { $bytes=[IO.File]::ReadAllBytes((Join-Path $output $name)); $entryStream.Write($bytes,0,$bytes.Length) } finally { $entryStream.Dispose() }
    }
} finally { $archive.Dispose(); $stream.Dispose() }
"Generated $archivePath with $($tasks.Count) tasks. No remote writes performed."
