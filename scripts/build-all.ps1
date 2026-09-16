<#
.SYNOPSIS
    Build every target, on machines that can actually build them.

.DESCRIPTION
    The engine cannot be cross-compiled: PyInstaller freezes with the interpreter it
    runs on, and the Mac app needs Xcode, which needs a Mac. So rather than pretend a
    Windows box can produce a Mac build, this starts the Build all workflow on GitHub's
    runners and, with -Wait, brings the finished artifacts back here.

    Needs the GitHub CLI (https://cli.github.com) and a push to have happened: the
    workflow builds what is on the branch, not what is in your working tree.

.PARAMETER Targets
    all (default), windows-x64, windows-arm64 or macos.

.PARAMETER Wait
    Follow the run and download what it produces into build\remote.

.EXAMPLE
    .\scripts\build-all.ps1
    .\scripts\build-all.ps1 -Targets macos -Wait
#>
[CmdletBinding()]
param(
    [ValidateSet('all', 'windows-x64', 'windows-arm64', 'macos')]
    [string]$Targets = 'all',
    [switch]$Wait
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$branch = (& git -C $repoRoot rev-parse --abbrev-ref HEAD).Trim()

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host ''
    Write-Host 'The GitHub CLI is not installed, so this cannot start the build for you.'
    Write-Host ''
    Write-Host 'Either install it:'
    Write-Host '    winget install GitHub.cli'
    Write-Host ''
    Write-Host 'or start the build in a browser:'
    Write-Host "    Actions -> Build all -> Run workflow -> $branch"
    Write-Host ''
    throw 'no gh'
}

if (& git -C $repoRoot status --porcelain) {
    Write-Host "note: you have uncommitted changes; the runners build $branch as pushed."
}

Write-Host "==> Starting Build all ($Targets) on $branch"
& gh workflow run build-all.yml --ref $branch -f "targets=$Targets"
if ($LASTEXITCODE -ne 0) { throw 'could not start the workflow' }

# The run takes a moment to appear, and asking too early finds the previous one.
Start-Sleep -Seconds 5
$runId = (& gh run list --workflow build-all.yml --branch $branch --limit 1 `
        --json databaseId --jq '.[0].databaseId').Trim()
$url = (& gh run view $runId --json url --jq .url).Trim()
Write-Host "==> Run ${runId}: $url"

if (-not $Wait) {
    Write-Host '    (pass -Wait to follow it and download what it builds)'
    exit 0
}

& gh run watch $runId --exit-status
if ($LASTEXITCODE -ne 0) { throw 'the build failed; see the run above' }

$destination = Join-Path $repoRoot 'build\remote'
New-Item -ItemType Directory -Force -Path $destination | Out-Null
& gh run download $runId --dir $destination
Write-Host "==> Downloaded into $destination"
Get-ChildItem -Path $destination -Recurse -File | ForEach-Object { Write-Host "    $($_.FullName)" }
