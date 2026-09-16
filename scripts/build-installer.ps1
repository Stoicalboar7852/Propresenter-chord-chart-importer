<#
.SYNOPSIS
    Package a built app folder into a Windows installer (.msi).

.DESCRIPTION
    Uses WiX, which installs as a .NET tool, so the .NET 8 SDK the app already needs is
    the only prerequisite: no separate installer toolchain, no admin rights.

    The result is per-user. It installs into %LOCALAPPDATA%\Programs\PCCI, adds a Start
    menu shortcut and an entry in Apps and Features, and never shows a UAC prompt. That
    is on purpose for an unsigned package: Windows cannot vouch for it, so it should not
    also be asking for administrator.

    There is no code-signing certificate for this project, so SmartScreen warns on first
    run whichever way it is packaged. See docs/INSTALL_WINDOWS.md.

.PARAMETER Source
    The finished app folder to package: the app, the engine beside it, nothing else.

.PARAMETER Output
    Where to write the .msi.

.PARAMETER Architecture
    win-x64 (default) or win-arm64. An x64 installer refuses to install on ARM64 and
    the other way round, so this has to match the build.

.PARAMETER Version
    Four-part product version. Installing a higher one replaces a lower one.

.EXAMPLE
    .\scripts\build-installer.ps1 -Source build\windows\win-x64 -Output build\windows\PCCI-x64.msi
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$Output,

    [ValidateSet('win-x64', 'win-arm64')]
    [string]$Architecture = 'win-x64',

    [string]$Version = '0.1.0.0'
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$authoring = Join-Path $repoRoot 'installer\windows\Pcci.wxs'
$icon = Join-Path $repoRoot 'windows\Pcci\Assets\AppIcon.ico'

if (-not (Test-Path $Source)) { Write-Error "nothing to package at $Source" }
if (-not (Test-Path $authoring)) { Write-Error "installer authoring is missing: $authoring" }
if (-not (Test-Path $icon)) { Write-Error "the app icon is missing: $icon" }

$sourceFull = (Resolve-Path $Source).Path
if (-not (Get-ChildItem -LiteralPath $sourceFull -File -Recurse | Select-Object -First 1)) {
    Write-Error "$sourceFull is empty"
}

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
    Write-Error 'dotnet not found: install the .NET 8 SDK (winget install Microsoft.DotNet.SDK.8)'
}

# WiX is a .NET tool rather than a separate download. Installing it needs no admin, and
# a machine that already has it says so on stderr rather than failing.
if (-not (Get-Command wix -ErrorAction SilentlyContinue)) {
    Write-Host '==> Installing the WiX toolset (dotnet tool, no admin needed)'
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & dotnet tool install --global wix --version 5.* 2>&1 | ForEach-Object { "$_" }
    }
    finally {
        $ErrorActionPreference = $previous
    }
    # A freshly installed global tool lands in a folder this session may not have on
    # PATH yet.
    $toolPath = Join-Path $env:USERPROFILE '.dotnet\tools'
    if ((Test-Path $toolPath) -and ($env:PATH -notlike "*$toolPath*")) {
        $env:PATH = "$toolPath;$env:PATH"
    }
    if (-not (Get-Command wix -ErrorAction SilentlyContinue)) {
        Write-Error 'could not install WiX; run: dotnet tool install --global wix'
    }
}

$wixArchitecture = if ($Architecture -eq 'win-arm64') { 'arm64' } else { 'x64' }
$outputDirectory = Split-Path -Parent $Output
if ($outputDirectory -and -not (Test-Path $outputDirectory)) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
}
if (Test-Path $Output) { Remove-Item -Force $Output }

Write-Host "==> Building $Output ($wixArchitecture)"
& wix build $authoring `
    -arch $wixArchitecture `
    -define "SourceFolder=$sourceFull" `
    -define "IconFile=$icon" `
    -define "Version=$Version" `
    -out $Output
if ($LASTEXITCODE -ne 0) { Write-Error 'wix build failed' }
if (-not (Test-Path $Output)) { Write-Error "wix reported success but wrote no $Output" }

# An MSI is a compound file; every one starts with the same eight bytes. Checking them
# is cheap, and a truncated installer that looks fine until somebody runs it is not.
$signature = [System.IO.File]::ReadAllBytes($Output)[0..7]
$expected = @(0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1)
if (Compare-Object $signature $expected) {
    Write-Error "$Output does not look like an MSI"
}

$size = [math]::Round((Get-Item $Output).Length / 1MB, 1)
Write-Host "==> Installer built: $Output ($size MB, per-user, unsigned)"
