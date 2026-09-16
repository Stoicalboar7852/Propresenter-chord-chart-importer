<#
.SYNOPSIS
    Create the engine's Python environment.

.DESCRIPTION
    Finds a Python new enough to run the engine, makes core\.venv, installs everything,
    and checks the result works. The build scripts call this when the environment is
    missing, so you should rarely need to run it by hand.

.PARAMETER Architecture
    win-x64 or win-arm64. Picks a Python of that architecture when the machine has
    more than one, so the frozen engine matches the app it ships inside. Defaults to
    this machine's architecture.

.EXAMPLE
    .\scripts\setup-engine.ps1
    .\scripts\setup-engine.ps1 -Architecture win-arm64
#>
[CmdletBinding()]
param(
    [ValidateSet('win-x64', 'win-arm64')]
    [string]$Architecture
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$core = Join-Path $repoRoot 'core'
$venv = Join-Path $core '.venv'

if (-not (Test-Path (Join-Path $core 'pyproject.toml'))) {
    Write-Host @'

core\pyproject.toml is missing, so this checkout does not contain the engine.

This usually means the checkout predates the engine landing on the default branch.
Bring it up to date:

    git fetch origin
    git checkout claude/blissful-planck-pbslml
    git pull

'@
    throw 'the engine is not in this checkout'
}

#region discovery

# Running a Python that turns out not to exist, or that is the Microsoft Store stub, is
# a normal part of looking for one. Windows PowerShell turns a native program's stderr
# into a terminating error when $ErrorActionPreference is 'Stop' and the stream is
# redirected, so every probe goes through here: preference lowered, output captured,
# nothing thrown. The caller gets plain strings and decides for itself.
function Invoke-Native {
    param(
        [string]$Executable,
        [string[]]$Arguments = @()
    )

    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $output = & $Executable @Arguments 2>&1
    }
    catch {
        $output = @()
    }
    finally {
        $ErrorActionPreference = $previous
    }
    return @($output | ForEach-Object { "$_" })
}

# platform.machine() as the -Architecture parameter spells it. 32-bit Pythons report
# 'x86' and fall through to '', which never matches a target and so sorts last.
function ConvertTo-BuildArchitecture {
    param([string]$Machine)

    switch ($Machine.ToUpperInvariant()) {
        'ARM64' { return 'win-arm64' }
        'AMD64' { return 'win-x64' }
        'X86_64' { return 'win-x64' }
        default { return '' }
    }
}

function Get-HostArchitecture {
    try {
        $osArchitecture = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
        if ($osArchitecture -eq 'Arm64') { return 'win-arm64' }
        if ($osArchitecture -eq 'X64') { return 'win-x64' }
    }
    catch {
        # .NET too old to answer; the environment below still can.
    }
    # PROCESSOR_ARCHITECTURE describes the current process, which is x86 when a 32-bit
    # PowerShell runs on a 64-bit machine. PROCESSOR_ARCHITEW6432 is the real one.
    $raw = $env:PROCESSOR_ARCHITEW6432
    if (-not $raw) { $raw = $env:PROCESSOR_ARCHITECTURE }
    if ($raw -eq 'ARM64') { return 'win-arm64' }
    return 'win-x64'
}

# Ask an interpreter what it is. Returns $null for anything that is not a working
# Python: a path that no longer exists, the Store stub, a launcher with nothing to
# launch. Identified by a marker line so that banners and warnings cannot be mistaken
# for the answer.
function Get-PythonInfo {
    param([string]$Executable)

    # Single quotes inside the Python, deliberately. Windows PowerShell hands arguments
    # to native programs by the old rules, which do not escape an embedded double quote:
    # Python would receive the format string unquoted and refuse to parse it.
    $probe = "import platform, sys; print('PCCIPY|%d.%d.%d|%s|%s' % (sys.version_info[0], sys.version_info[1], sys.version_info[2], platform.machine(), sys.executable))"
    $lines = Invoke-Native $Executable @('-c', $probe)
    foreach ($line in $lines) {
        if ($line -notmatch '^PCCIPY\|') { continue }
        $fields = $line.Split('|')
        if ($fields.Count -lt 4) { continue }
        $version = $null
        if (-not [version]::TryParse($fields[1], [ref]$version)) { continue }
        return [pscustomobject]@{
            Version = $version
            Machine = $fields[2]
            Arch    = ConvertTo-BuildArchitecture $fields[2]
            Path    = $fields[3]
        }
    }
    return $null
}

# Every interpreter worth asking about, as a path or a bare command name.
function Get-PythonCandidates {
    $candidates = @()

    if (Get-Command py -ErrorAction SilentlyContinue) {
        # `py -0p` lists every registered install with its path. Ask it rather than
        # guessing version flags: an ARM64 install registers as 3.12-arm64, which a
        # bare `py -3.12` does not match, and that is how this script used to fail.
        foreach ($line in (Invoke-Native 'py' @('-0p'))) {
            $match = [regex]::Match($line, '(?<path>[A-Za-z]:\\[^"<>|]*?python\.exe)')
            if ($match.Success) { $candidates += $match.Groups['path'].Value }
        }
        # Whatever the launcher picks by default, in case the listing said nothing
        # useful. It reports its own sys.executable, so this still resolves to a path.
        $candidates += 'py'
    }

    foreach ($name in @('python3.14', 'python3.13', 'python3.12', 'python3', 'python')) {
        $command = Get-Command $name -ErrorAction SilentlyContinue
        if ($command -and $command.Path) { $candidates += $command.Path }
    }

    # Installers that were never added to PATH, and a py launcher that does not know
    # about them either.
    $roots = @()
    if ($env:LOCALAPPDATA) { $roots += (Join-Path $env:LOCALAPPDATA 'Programs\Python') }
    if ($env:ProgramFiles) { $roots += $env:ProgramFiles }
    if (${env:ProgramFiles(x86)}) { $roots += ${env:ProgramFiles(x86)} }
    if ($env:SystemDrive) { $roots += "$env:SystemDrive\" }
    foreach ($root in $roots) {
        if (-not (Test-Path $root)) { continue }
        $directories = Get-ChildItem -LiteralPath $root -Filter 'Python3*' -Directory `
            -ErrorAction SilentlyContinue
        foreach ($directory in $directories) {
            $executable = Join-Path $directory.FullName 'python.exe'
            if (Test-Path $executable) { $candidates += $executable }
        }
    }

    return @($candidates)
}

function Find-Python {
    param([string]$Target)

    $found = @()
    $seen = @{}
    foreach ($candidate in @(Get-PythonCandidates)) {
        $info = Get-PythonInfo $candidate
        if (-not $info) { continue }
        $key = $info.Path.ToLowerInvariant()
        if ($seen.ContainsKey($key)) { continue }
        $seen[$key] = $true
        $found += $info
    }

    # Matching architecture first, then newest. A 3.13 that is present beats a 3.12
    # that is also present.
    $usable = @($found | Where-Object { $_.Version -ge [version]'3.12' })
    $best = $usable |
        Sort-Object `
            @{ Expression = { if ($_.Arch -eq $Target) { 0 } else { 1 } } }, `
            @{ Expression = { $_.Version }; Descending = $true } |
        Select-Object -First 1

    return [pscustomobject]@{
        Best  = $best
        Found = $found
    }
}

#endregion discovery

$target = $Architecture
if (-not $target) { $target = Get-HostArchitecture }

Write-Host '==> Looking for Python 3.12 or newer'
$search = Find-Python -Target $target
$python = $search.Best

if (-not $python) {
    Write-Host ''
    Write-Host 'The engine needs Python 3.12 or newer, and this machine does not have one.'
    if ($search.Found.Count -gt 0) {
        Write-Host ''
        Write-Host 'What it found, all too old:'
        foreach ($candidate in $search.Found) {
            Write-Host "    $($candidate.Version) at $($candidate.Path)"
        }
    }
    Write-Host @'

Install a current one with winget:

    winget install Python.Python.3.12

or download an installer from https://www.python.org/downloads/

Then run this script again.

'@
    throw 'no Python 3.12 or newer'
}

Write-Host "==> Using Python $($python.Version) ($($python.Machine)) at $($python.Path)"
if ($python.Arch -ne $target) {
    Write-Host "    note: this is not a $target Python, so the engine will be built for" `
        "$($python.Machine). It still runs, but install a $target Python to match the app."
}

if (Test-Path $venv) {
    Write-Host '==> Removing the previous environment at core\.venv'
    Remove-Item -Recurse -Force $venv
}

Write-Host '==> Creating core\.venv'
& $python.Path -m venv $venv
if ($LASTEXITCODE -ne 0) { Write-Error 'could not create the virtual environment' }

$venvPython = Join-Path $venv 'Scripts\python.exe'
if (-not (Test-Path $venvPython)) { Write-Error "no interpreter at $venvPython" }

Write-Host '==> Installing the engine and its tooling (this takes a minute)'
& $venvPython -m pip install --quiet --upgrade pip
if ($LASTEXITCODE -ne 0) { Write-Error 'could not upgrade pip' }
& $venvPython -m pip install --quiet -e "$core[dev]"
if ($LASTEXITCODE -ne 0) { Write-Error 'installation failed' }

Write-Host '==> Checking it works'
& (Join-Path $venv 'Scripts\pcci.exe') doctor
if ($LASTEXITCODE -ne 0) { Write-Error 'the engine failed its own doctor check' }

Write-Host @'

Ready. Useful commands:

    core\.venv\Scripts\pcci convert "My Song.docx" -o "My Song.pro"
    core\.venv\Scripts\python -m pytest       (from inside core\)
    .\scripts\build-windows.ps1               builds the app, engine included
'@
