<#
.SYNOPSIS
    Create the engine's Python environment.

.DESCRIPTION
    Finds a Python new enough to run the engine, makes core\.venv, installs everything,
    and checks the result works. The build scripts call this when the environment is
    missing, so you should rarely need to run it by hand.

.EXAMPLE
    .\scripts\setup-engine.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$core = Join-Path $repoRoot 'core'
$venv = Join-Path $core '.venv'

if (-not (Test-Path (Join-Path $core 'pyproject.toml'))) {
    Write-Error @'
core\pyproject.toml is missing, so this checkout does not contain the engine.

This usually means the checkout predates the engine landing on the default branch.
Bring it up to date:

    git fetch origin
    git checkout claude/blissful-planck-pbslml
    git pull
'@
}

function Find-Python {
    # The py launcher knows about every installed version; ask it first.
    if (Get-Command py -ErrorAction SilentlyContinue) {
        foreach ($version in @('3.13', '3.12')) {
            & py "-$version" -c 'import sys' 2>$null
            if ($LASTEXITCODE -eq 0) { return @('py', "-$version") }
        }
    }
    foreach ($candidate in @('python3.13', 'python3.12', 'python3', 'python')) {
        if (-not (Get-Command $candidate -ErrorAction SilentlyContinue)) { continue }
        & $candidate -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' 2>$null
        if ($LASTEXITCODE -eq 0) { return @($candidate) }
    }
    return $null
}

$python = Find-Python
if (-not $python) {
    Write-Error @'
The engine needs Python 3.12 or newer, and this machine does not have one.

Install it with winget:

    winget install Python.Python.3.12

or download an installer from https://www.python.org/downloads/

Then run this script again.
'@
}

Write-Host "==> Using $($python -join ' ')"

if (Test-Path $venv) {
    Write-Host '==> Removing the previous environment at core\.venv'
    Remove-Item -Recurse -Force $venv
}

Write-Host '==> Creating core\.venv'
& $python[0] @($python[1..($python.Count - 1)]) -m venv $venv
if ($LASTEXITCODE -ne 0) { Write-Error 'could not create the virtual environment' }

$venvPython = Join-Path $venv 'Scripts\python.exe'
Write-Host '==> Installing the engine and its tooling (this takes a minute)'
& $venvPython -m pip install --quiet --upgrade pip
& $venvPython -m pip install --quiet -e "$core[dev]"
if ($LASTEXITCODE -ne 0) { Write-Error 'installation failed' }

Write-Host '==> Checking it works'
& (Join-Path $venv 'Scripts\pcci.exe') doctor

Write-Host @'

Ready. Useful commands:

    core\.venv\Scripts\pcci convert "My Song.docx" -o "My Song.pro"
    core\.venv\Scripts\python -m pytest       (from inside core\)
    .\scripts\build-windows.ps1               builds the app, engine included
'@
