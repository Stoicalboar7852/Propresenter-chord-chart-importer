# Installing PCCI on Windows

The app is **not code-signed**, because this project has no certificate. It runs fine;
SmartScreen just needs one extra click the first time.

## Build it

```powershell
git clone https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer.git
cd Propresenter-chord-chart-importer

.\scripts\build-windows.ps1
```

That is the whole thing. The build script sets up the engine's Python environment the
first time. To do only that step — to run the command-line tool without building an
app — use `.\scripts\setup-engine.ps1`.

The result is `build\windows\win-x64\` and a zip beside it. Copy the folder wherever
you like; it is self-contained and needs no installer.

Requirements: Windows 10 1809 or later, the .NET 8 SDK, and **Python 3.12 or newer**
(`winget install Python.Python.3.12`). For an ARM machine:
`.\scripts\build-windows.ps1 -Architecture win-arm64`.

## First launch

Windows will show **"Windows protected your PC"**. Click **More info**, then **Run
anyway**. Once only.

If the zip came from a browser or email, Windows may also block the files inside it.
Right-click the zip → **Properties** → tick **Unblock** → **OK**, then extract it.

## What is inside

```
PCCI.exe            the app
engine\pcci.exe     the frozen conversion engine (about 120 MB)
STAGE_SETUP.md
```

The engine is an ordinary command-line program, useful when something is wrong:

```powershell
.\engine\pcci.exe doctor
.\engine\pcci.exe convert "My Song.docx" -o "My Song.pro"
```

Logs go to `%LOCALAPPDATA%\PCCI\Logs\pcci.log`. They record paths and structure only,
never the contents of your charts.

## If you later get a certificate

```powershell
signtool sign /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 `
  /f certificate.pfx /p PASSWORD build\windows\win-x64\PCCI.exe
```

Sign `engine\pcci.exe` as well. With a certificate an MSIX becomes worthwhile too;
without one it is strictly worse than the folder, because MSIX refuses to install
unsigned.
