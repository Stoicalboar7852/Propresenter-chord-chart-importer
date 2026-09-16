<#
.SYNOPSIS
    Test the interpreter discovery inside setup-engine.ps1.

.DESCRIPTION
    setup-engine.ps1 has to look for Python on machines it cannot see, so the parts
    that decide what counts as an interpreter are tested here instead. Runs anywhere
    PowerShell does, needs nothing installed beyond a python3 on PATH, and fails loudly.

.EXAMPLE
    pwsh -File scripts\test-setup-engine.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$setup = Join-Path $PSScriptRoot 'setup-engine.ps1'
$source = Get-Content $setup -Raw
$region = [regex]::Match($source, '(?s)#region discovery(?<body>.*?)#endregion discovery')
if (-not $region.Success) {
    throw "setup-engine.ps1 has no #region discovery block to test"
}
. ([scriptblock]::Create($region.Groups['body'].Value))

$failures = @()
function Assert-That {
    param([string]$Name, [bool]$Condition, [string]$Detail = '')

    if ($Condition) {
        Write-Host "  ok    $Name"
    }
    else {
        Write-Host "  FAIL  $Name$(if ($Detail) { " — $Detail" })"
        $script:failures += $Name
    }
}

Write-Host 'py -0p parsing'
# Both launcher formats, a path with a space in it, and the lines that are not paths.
$listing = @(
    'Installed Pythons found by py Launcher for Windows',
    ' -V:3.12-arm64 *        C:\Users\someone\AppData\Local\Programs\Python\Python312-arm64\python.exe',
    ' -V:3.11                C:\Program Files\Python311\python.exe',
    ' -3.8-64        C:\Python38\python.exe *',
    ' -V:3.12-arm64          C:\Users\someone\Python312-arm64\pythonw.exe',
    'No suitable Python runtime found'
)
$parsed = @()
foreach ($line in $listing) {
    $match = [regex]::Match($line, '(?<path>[A-Za-z]:\\[^"<>|]*?python\.exe)')
    if ($match.Success) { $parsed += $match.Groups['path'].Value }
}
Assert-That 'finds the architecture-tagged install' `
    ($parsed -contains 'C:\Users\someone\AppData\Local\Programs\Python\Python312-arm64\python.exe')
Assert-That 'keeps a path containing a space' `
    ($parsed -contains 'C:\Program Files\Python311\python.exe')
Assert-That 'handles the older -3.8-64 listing' ($parsed -contains 'C:\Python38\python.exe')
Assert-That 'ignores pythonw.exe and prose' ($parsed.Count -eq 3) "parsed $($parsed.Count)"

Write-Host 'architecture mapping'
Assert-That 'ARM64 maps to win-arm64' ((ConvertTo-BuildArchitecture 'ARM64') -eq 'win-arm64')
Assert-That 'AMD64 maps to win-x64' ((ConvertTo-BuildArchitecture 'AMD64') -eq 'win-x64')
Assert-That '32-bit maps to nothing' ((ConvertTo-BuildArchitecture 'x86') -eq '')
Assert-That 'the host answers with one of the two' `
    (@('win-x64', 'win-arm64') -contains (Get-HostArchitecture))

Write-Host 'probing an interpreter'
$real = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $real) { $real = Get-Command python -ErrorAction SilentlyContinue }
if (-not $real) { throw 'no python3 or python on PATH to test against' }

$info = Get-PythonInfo $real.Path
Assert-That 'reports a version' ($null -ne $info -and $info.Version.Major -eq 3)
Assert-That 'reports an absolute path' ($null -ne $info -and (Test-Path $info.Path))
# The fields are positional, so a shifted index shows up as a path where the machine
# name should be.
Assert-That 'reports a machine, not a path' `
    ($null -ne $info -and $info.Machine -and $info.Machine -notmatch '[\\/]') `
    "machine was '$($info.Machine)'"
Assert-That 'the path is the interpreter' `
    ($null -ne $info -and (Split-Path -Leaf $info.Path) -match '^python')

# Looking for Python means running things that turn out not to be Python. None of it
# may throw, whatever the shell's error preference: this is what used to abort the
# script on a machine whose py launcher answered "No suitable Python runtime found".
Assert-That 'a missing interpreter is skipped, not thrown' `
    ($null -eq (Get-PythonInfo (Join-Path $PSScriptRoot 'no-such-python.exe')))
# This very PowerShell: a real program that runs, rejects the argument, writes to
# stderr and is not Python. Windows PowerShell turns that stderr into a terminating
# error unless the probe guards against it.
Assert-That 'a program that is not Python is skipped' `
    ($null -eq (Get-PythonInfo (Get-Process -Id $PID).Path))

Write-Host 'selection'
# Exactly one candidate is its own case: a function returning a single-element
# collection unrolls it, which once turned the only interpreter on the machine into
# the first character of its own path.
function Get-PythonCandidates { return @($real.Path) }
$search = Find-Python -Target (Get-HostArchitecture)
Assert-That 'a lone candidate survives' ($search.Found.Count -eq 1) "found $($search.Found.Count)"

function Get-PythonCandidates { return @($real.Path, $real.Path) }
$search = Find-Python -Target (Get-HostArchitecture)
Assert-That 'the same interpreter twice counts once' ($search.Found.Count -eq 1)

function Get-PythonCandidates { return @() }
$search = Find-Python -Target 'win-x64'
Assert-That 'nothing found is not an error' `
    ($null -eq $search.Best -and $search.Found.Count -eq 0)

# Ordering, without needing four Pythons installed to check it.
$records = @(
    [pscustomobject]@{ Version = [version]'3.13.1'; Arch = 'win-x64'; Path = 'C:\a\python.exe' },
    [pscustomobject]@{ Version = [version]'3.12.10'; Arch = 'win-arm64'; Path = 'C:\b\python.exe' },
    [pscustomobject]@{ Version = [version]'3.11.9'; Arch = 'win-arm64'; Path = 'C:\c\python.exe' },
    [pscustomobject]@{ Version = [version]'3.14.0'; Arch = 'win-arm64'; Path = 'C:\d\python.exe' }
)
$usable = @($records | Where-Object { $_.Version -ge [version]'3.12' })
Assert-That '3.11 is not usable' ($usable.Count -eq 3)
foreach ($case in @(
        @{ Target = 'win-arm64'; Expected = '3.14.0' },
        @{ Target = 'win-x64'; Expected = '3.13.1' })) {
    $best = $usable |
        Sort-Object `
            @{ Expression = { if ($_.Arch -eq $case.Target) { 0 } else { 1 } } }, `
            @{ Expression = { $_.Version }; Descending = $true } |
        Select-Object -First 1
    Assert-That "$($case.Target) picks $($case.Expected)" `
        ("$($best.Version)" -eq $case.Expected) "picked $($best.Version)"
}

Write-Host ''
if ($failures.Count -gt 0) {
    throw "$($failures.Count) check(s) failed: $($failures -join ', ')"
}
Write-Host 'All discovery checks passed.'
