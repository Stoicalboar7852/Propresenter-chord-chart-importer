<#
.SYNOPSIS
    Build the Windows app with the engine inside it.

.DESCRIPTION
    Produces a self-contained folder and a zip. There is no code-signing certificate for
    this project, so the result is unsigned: SmartScreen will warn on first run. See
    docs/INSTALL_WINDOWS.md.

.PARAMETER Architecture
    win-x64 (default) or win-arm64.

.PARAMETER NoInstaller
    Skip the .msi and produce only the portable folder and zip.

.PARAMETER InstallMissing
    Install anything this machine is missing (Python, the .NET SDK) without asking.

.EXAMPLE
    .\scripts\build-windows.ps1
    .\scripts\build-windows.ps1 -Architecture win-arm64
#>
[CmdletBinding()]
param(
    [ValidateSet('win-x64', 'win-arm64')]
    [string]$Architecture = 'win-x64',
    [switch]$SkipEngine,
    [switch]$NoInstaller,
    [switch]$InstallMissing
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$project = Join-Path $repoRoot 'windows\Pcci\Pcci.csproj'
$output = Join-Path $repoRoot "build\windows\$Architecture"
$engineOutput = Join-Path $repoRoot 'build\engine'

if ($InstallMissing) {
    & (Join-Path $PSScriptRoot 'install-deps.ps1') -Yes
}

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
    Write-Host ''
    Write-Host 'The .NET 8 SDK is not on this machine, and the app cannot be built without it.'
    Write-Host ''
    Write-Host '    .\scripts\install-deps.ps1        checks and offers to install it'
    Write-Host '    winget install Microsoft.DotNet.SDK.8'
    Write-Host ''
    Write-Host 'The engine does not need it: .\scripts\setup-engine.ps1 then'
    Write-Host 'core\.venv\Scripts\pcci convert "My Song.docx" -o "My Song.pro"'
    Write-Host ''
    throw 'no .NET SDK'
}

if (-not $SkipEngine) {
    Write-Host '==> Building the engine'
    & (Join-Path $PSScriptRoot 'build-engine.ps1') -OutputDirectory $engineOutput `
        -Architecture $Architecture
}

Write-Host "==> Publishing the app ($Architecture)"
if (Test-Path $output) { Remove-Item -Recurse -Force $output }
& dotnet publish $project `
    -c Release `
    -r $Architecture `
    --self-contained true `
    -o $output
if ($LASTEXITCODE -ne 0) { Write-Error 'dotnet publish failed' }

Write-Host '==> Bundling the engine'
$engineSource = Join-Path $engineOutput 'pcci'
if (-not (Test-Path $engineSource)) { Write-Error "engine not found at $engineSource" }
Copy-Item -Recurse -Force $engineSource (Join-Path $output 'engine')
Copy-Item -Force (Join-Path $repoRoot 'docs\STAGE_SETUP.md') $output

Write-Host '==> Checking the bundled engine runs'
$bundled = Join-Path $output 'engine\pcci.exe'
$doctor = & $bundled doctor --json | ConvertFrom-Json
if (-not $doctor.ok) { Write-Error 'the bundled engine failed its doctor check' }

$zip = Join-Path $repoRoot "build\windows\PCCI-$Architecture.zip"
if (Test-Path $zip) { Remove-Item -Force $zip }
Compress-Archive -Path "$output\*" -DestinationPath $zip

# Both shapes, every time: a folder to unzip and run, and an installer for people who
# would rather have a Start menu entry and an uninstaller.
$installer = Join-Path $repoRoot "build\windows\PCCI-$Architecture-setup.exe"
if (-not $NoInstaller) {
    & (Join-Path $PSScriptRoot 'build-installer.ps1') `
        -Source $output -Output $installer -Architecture $Architecture
}

Write-Host "==> Built $output"
Write-Host "==> Zipped $zip"
if (-not $NoInstaller) { Write-Host "==> Installer $installer" }
Write-Host ''
Write-Host 'Unsigned build: Windows SmartScreen will warn on first launch.'
Write-Host 'See docs/INSTALL_WINDOWS.md for what to tell people.'
