<#
.SYNOPSIS
    Check this machine can build PCCI, and install what it is missing.

.DESCRIPTION
    Two things are needed to build the Windows app: Python 3.12 or newer for the
    engine, and the .NET 8 SDK for the app itself. This reports on both and offers to
    install whichever is absent, through winget.

    Nothing is installed without being asked first, unless -Yes is passed. Installing
    software on somebody's machine is not a thing to do quietly.

    The WiX toolset, which builds the installer, is not listed here: it is a dotnet
    tool, so scripts\build-installer.ps1 fetches it when it needs it.

.PARAMETER Yes
    Install what is missing without asking. For unattended runs.

.PARAMETER CheckOnly
    Report and exit; install nothing. Exit code 1 if anything is missing.

.EXAMPLE
    .\scripts\install-deps.ps1
    .\scripts\install-deps.ps1 -Yes
#>
[CmdletBinding()]
param(
    [switch]$Yes,
    [switch]$CheckOnly
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$setup = Join-Path $PSScriptRoot 'setup-engine.ps1'

# The interpreter hunt lives in setup-engine.ps1 and is borrowed rather than copied:
# two implementations of "is there a Python here" would disagree eventually, and the
# one over there is the one with tests against it.
$source = Get-Content $setup -Raw
$region = [regex]::Match($source, '(?s)#region discovery(?<body>.*?)#endregion discovery')
if (-not $region.Success) { Write-Error "setup-engine.ps1 has no discovery block to borrow" }
. ([scriptblock]::Create($region.Groups['body'].Value))

function Get-DotnetSdk {
    <#
        .SYNOPSIS
            The newest .NET SDK major version installed, or 0 for none.
    #>
    if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) { return 0 }
    $newest = 0
    foreach ($line in (Invoke-Native 'dotnet' @('--list-sdks'))) {
        $match = [regex]::Match($line, '^(?<major>\d+)\.')
        if ($match.Success) {
            $major = [int]$match.Groups['major'].Value
            if ($major -gt $newest) { $newest = $major }
        }
    }
    return $newest
}

Write-Host '==> Checking what this machine has'

$missing = @()

$python = (Find-Python -Target (Get-HostArchitecture)).Best
if ($python) {
    Write-Host "  ok    Python $($python.Version) ($($python.Machine)) at $($python.Path)"
}
else {
    Write-Host '  MISSING  Python 3.12 or newer'
    $missing += [pscustomobject]@{
        Name    = 'Python 3.12'
        Package = 'Python.Python.3.12'
        Why     = 'the conversion engine'
    }
}

$sdk = Get-DotnetSdk
if ($sdk -ge 8) {
    Write-Host "  ok    .NET SDK $sdk"
}
else {
    Write-Host '  MISSING  .NET 8 SDK'
    $missing += [pscustomobject]@{
        Name    = '.NET 8 SDK'
        Package = 'Microsoft.DotNet.SDK.8'
        Why     = 'the Windows app (the engine alone does not need it)'
    }
}

if ($missing.Count -eq 0) {
    Write-Host ''
    Write-Host 'Everything needed is here. Next:'
    Write-Host '    .\scripts\build-windows.ps1'
    exit 0
}

Write-Host ''
Write-Host 'Missing:'
foreach ($item in $missing) {
    Write-Host "  $($item.Name)  -  $($item.Why)"
}

if ($CheckOnly) { exit 1 }

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host ''
    Write-Host 'winget is not on this machine, so these cannot be installed automatically.'
    Write-Host 'Install App Installer from the Microsoft Store, or download each directly:'
    Write-Host '    Python   https://www.python.org/downloads/'
    Write-Host '    .NET 8   https://dotnet.microsoft.com/download/dotnet/8.0'
    exit 1
}

if (-not $Yes) {
    Write-Host ''
    $answer = Read-Host "Install $($missing.Count) package(s) with winget now? [y/N]"
    if ($answer -notmatch '^(y|yes)$') {
        Write-Host 'Nothing installed.'
        exit 1
    }
}

foreach ($item in $missing) {
    Write-Host ""
    Write-Host "==> winget install $($item.Package)"
    # winget is chatty on stderr even when it succeeds, and Windows PowerShell turns
    # that into a terminating error under 'Stop'.
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & winget install --id $item.Package --exact --source winget `
            --accept-package-agreements --accept-source-agreements 2>&1 |
            ForEach-Object { "$_" }
    }
    finally {
        $ErrorActionPreference = $previous
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    winget exited with $LASTEXITCODE for $($item.Name)"
    }
}

Write-Host ''
Write-Host 'Installed. A new terminal may be needed before PATH catches up, then:'
Write-Host '    .\scripts\build-windows.ps1'
Write-Host ''
Write-Host 'Run this again to confirm:'
Write-Host '    .\scripts\install-deps.ps1 -CheckOnly'
