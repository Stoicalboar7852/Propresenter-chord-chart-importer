<#
.SYNOPSIS
    Package a built app folder into a Windows installer.

.DESCRIPTION
    Produces a setup .exe that asks where to go rather than deciding for you:

      * all users (Program Files, needs administrator) or just you (your own folder,
        needs nothing);
      * any folder you like, on the directory page;
      * a desktop shortcut, optional. An all-users install puts it on the public
        desktop so everyone sees it; a personal install puts it on yours.

    Built with Inno Setup, which is installed automatically if this machine does not
    have it. There is no code-signing certificate for this project, so SmartScreen
    warns on first run whichever way it is packaged. See docs/INSTALL_WINDOWS.md.

.PARAMETER Source
    The finished app folder to package: the app, the engine beside it, nothing else.

.PARAMETER Output
    Where to write the setup .exe.

.PARAMETER Architecture
    win-x64 (default) or win-arm64. An ARM64 installer refuses to run on an Intel
    machine, so this has to match the build.

.PARAMETER Version
    Product version, shown in Apps and Features.

.EXAMPLE
    .\scripts\build-installer.ps1 -Source build\windows\win-x64 -Output build\windows\PCCI-x64-setup.exe
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$Output,

    [ValidateSet('win-x64', 'win-arm64')]
    [string]$Architecture = 'win-x64',

    [string]$Version = '0.2.0'
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$authoring = Join-Path $repoRoot 'installer\windows\Pcci.iss'

if (-not (Test-Path $Source)) { Write-Error "nothing to package at $Source" }
if (-not (Test-Path $authoring)) { Write-Error "installer authoring is missing: $authoring" }

$sourceFull = (Resolve-Path $Source).Path
if (-not (Get-ChildItem -LiteralPath $sourceFull -File -Recurse | Select-Object -First 1)) {
    Write-Error "$sourceFull is empty"
}
$icon = Join-Path $sourceFull 'Assets\AppIcon.ico'
if (-not (Test-Path $icon)) { Write-Error "the app icon is missing from the build: $icon" }

function Find-Iscc {
    <#
        .SYNOPSIS
            The Inno Setup compiler, or $null.
    #>
    $onPath = Get-Command iscc -ErrorAction SilentlyContinue
    if ($onPath) { return $onPath.Path }
    foreach ($root in @($env:ProgramFiles, ${env:ProgramFiles(x86)})) {
        if (-not $root) { continue }
        foreach ($version in @('6', '5')) {
            $candidate = Join-Path $root "Inno Setup $version\ISCC.exe"
            if (Test-Path $candidate) { return $candidate }
        }
    }
    return $null
}

function Invoke-Quietly {
    <#
        .SYNOPSIS
            Run a program whose chatter on stderr is not a failure.
    #>
    param([string]$Executable, [string[]]$Arguments)

    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & $Executable @Arguments 2>&1 | ForEach-Object { "    $_" }
    }
    finally {
        $ErrorActionPreference = $previous
    }
}

$iscc = Find-Iscc
if (-not $iscc) {
    Write-Host '==> Installing Inno Setup'
    # Chocolatey first: it is what build servers have, and it does not need a console
    # session the way winget sometimes does.
    if (Get-Command choco -ErrorAction SilentlyContinue) {
        Invoke-Quietly 'choco' @('install', 'innosetup', '-y', '--no-progress')
    }
    elseif (Get-Command winget -ErrorAction SilentlyContinue) {
        Invoke-Quietly 'winget' @(
            'install', '--id', 'JRSoftware.InnoSetup', '--exact', '--source', 'winget',
            '--accept-package-agreements', '--accept-source-agreements'
        )
    }
    $iscc = Find-Iscc
}

if (-not $iscc) {
    Write-Host ''
    Write-Host 'Inno Setup is needed to build the installer and could not be installed.'
    Write-Host 'Install it from https://jrsoftware.org/isdl.php and run this again, or'
    Write-Host 'build without one:'
    Write-Host ''
    Write-Host '    .\scripts\build-windows.ps1 -NoInstaller'
    Write-Host ''
    throw 'no Inno Setup'
}

$outputDirectory = Split-Path -Parent $Output
if (-not $outputDirectory) { $outputDirectory = '.' }
if (-not (Test-Path $outputDirectory)) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
}
$outputDirectory = (Resolve-Path $outputDirectory).Path
$outputName = [System.IO.Path]::GetFileNameWithoutExtension($Output)
$finalPath = Join-Path $outputDirectory "$outputName.exe"
if (Test-Path $finalPath) { Remove-Item -Force $finalPath }

# Not $architecture: PowerShell variable names are case-insensitive, so that would
# assign to the parameter above and fail its own ValidateSet.
$innoArchitecture = if ($Architecture -eq 'win-arm64') { 'arm64' } else { 'x64' }

Write-Host "==> Building $finalPath ($innoArchitecture)"
Write-Host "    with $iscc"
& $iscc `
    "/DSourceFolder=$sourceFull" `
    "/DOutputDir=$outputDirectory" `
    "/DOutputName=$outputName" `
    "/DAppVersion=$Version" `
    "/DArch=$innoArchitecture" `
    $authoring | ForEach-Object { if ($_ -match 'error|warning') { "    $_" } }
if ($LASTEXITCODE -ne 0) { Write-Error 'Inno Setup failed' }
if (-not (Test-Path $finalPath)) { Write-Error "the compiler reported success but wrote no $finalPath" }

# Every Windows executable starts MZ. A truncated installer that looks fine until
# somebody double-clicks it is not something to find out about later.
$signature = [System.IO.File]::ReadAllBytes($finalPath)[0..1]
if ($signature[0] -ne 0x4D -or $signature[1] -ne 0x5A) {
    Write-Error "$finalPath does not look like a Windows program"
}

$size = [math]::Round((Get-Item $finalPath).Length / 1MB, 1)
Write-Host "==> Installer built: $finalPath ($size MB, unsigned)"
Write-Host '    It asks where to install and offers a desktop shortcut.'
