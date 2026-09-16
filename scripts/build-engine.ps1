<#
.SYNOPSIS
    Freeze the pcci engine into a self-contained directory the Windows app can ship.

.DESCRIPTION
    onedir, not onefile: onefile unpacks to a temporary directory on every launch,
    which is slow and trips some antivirus heuristics.

.PARAMETER Architecture
    win-x64 or win-arm64. Only used when the Python environment has to be created:
    it picks an interpreter of that architecture so the frozen engine matches the app.

.EXAMPLE
    .\scripts\build-engine.ps1
#>
[CmdletBinding()]
param(
    [string]$OutputDirectory,

    [ValidateSet('win-x64', 'win-arm64')]
    [string]$Architecture
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$core = Join-Path $repoRoot 'core'
if (-not $OutputDirectory) { $OutputDirectory = Join-Path $repoRoot 'build\engine' }
$work = Join-Path $repoRoot 'build\pyinstaller'
$python = Join-Path $core '.venv\Scripts\python.exe'

if (-not (Test-Path $python)) {
    Write-Host '==> No Python environment yet; setting one up'
    $setupArguments = @{}
    if ($Architecture) { $setupArguments['Architecture'] = $Architecture }
    & (Join-Path $PSScriptRoot 'setup-engine.ps1') @setupArguments
    if (-not (Test-Path $python)) { Write-Error 'the environment was not created' }
}

# PyInstaller freezes with the interpreter it runs on, so an x64 environment produces an
# x64 engine however the app is published. Say so rather than shipping a mismatch.
if ($Architecture) {
    $machine = "$(& $python -c 'import platform; print(platform.machine())')".Trim()
    $wanted = if ($Architecture -eq 'win-arm64') { 'ARM64' } else { 'AMD64' }
    if ($machine -and $machine -ne $wanted) {
        Write-Host "    note: core\.venv runs a $machine Python, so the engine will be $machine and"
        Write-Host "          not $wanted. Delete core\.venv and run this again to pick a match."
    }
}

Write-Host '==> Installing PyInstaller'
& $python -m pip install --quiet --upgrade pyinstaller
if ($LASTEXITCODE -ne 0) { Write-Error 'could not install PyInstaller' }

if (Test-Path $OutputDirectory) { Remove-Item -Recurse -Force $OutputDirectory }
if (Test-Path $work) { Remove-Item -Recurse -Force $work }
New-Item -ItemType Directory -Force -Path $OutputDirectory, $work | Out-Null

# The generated protobuf modules are imported by bare name after their directory is
# added to sys.path at runtime, so PyInstaller cannot see them, or their dependency
# on google.protobuf, by static analysis. Both are declared explicitly. On Windows the
# --add-data separator is ';', not ':'.
$generated = 'pcci\propresenter\proto\generated'
$generatedSource = Join-Path $core $generated

Write-Host '==> Freezing the engine'
Push-Location $core
try {
    & $python -m PyInstaller `
        --noconfirm --clean --onedir --console `
        --name pcci `
        --distpath $OutputDirectory `
        --workpath $work `
        --specpath $work `
        --add-data "$generatedSource;$generated" `
        --hidden-import pcci.ingest.chordpro `
        --hidden-import pcci.ingest.docx `
        --hidden-import pcci.ingest.html `
        --hidden-import pcci.ingest.markdown `
        --hidden-import pcci.ingest.odt `
        --hidden-import pcci.ingest.pdf `
        --hidden-import pcci.ingest.rtf `
        --hidden-import pcci.ingest.txt `
        --collect-submodules pymupdf `
        --collect-submodules charset_normalizer `
        --collect-submodules google.protobuf `
        --copy-metadata protobuf `
        entrypoint.py
    if ($LASTEXITCODE -ne 0) { Write-Error 'PyInstaller failed' }
}
finally {
    Pop-Location
}

$binary = Join-Path $OutputDirectory 'pcci\pcci.exe'
if (-not (Test-Path $binary)) { Write-Error "Build produced no executable at $binary" }

# A frozen engine that cannot load its protobuf bindings looks fine until somebody
# tries to export, so the build fails here rather than in front of a congregation.
Write-Host '==> Smoke testing the frozen engine'
$doctor = & $binary doctor --json | ConvertFrom-Json
$failed = $doctor.checks | Where-Object { -not $_.ok }
if ($failed) {
    $failed | ForEach-Object { Write-Host "  FAIL $($_.check): $($_.detail)" }
    Write-Error 'the frozen engine failed its own doctor check'
}
Write-Host "  $($doctor.checks.Count) checks passed"

$sample = Join-Path $core 'tests\fixtures\chordpro\goodbye_yesterday.cho'
if (Test-Path $sample) {
    $smoke = Join-Path $work 'smoke.pro'
    & $binary convert $sample -o $smoke --json | Out-Null
    if (-not (Test-Path $smoke)) { Write-Error 'conversion smoke test wrote nothing' }
    Write-Host '  conversion smoke test passed'
}

Write-Host "==> Engine built: $OutputDirectory\pcci"
