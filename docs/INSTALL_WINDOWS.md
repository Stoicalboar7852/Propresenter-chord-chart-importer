# Installing PCCI on Windows

The app is **not code-signed**, because this project has no certificate. It runs fine;
SmartScreen just needs one extra click the first time.

## Build it

```powershell
git clone https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer.git
cd Propresenter-chord-chart-importer

.\scripts\install-deps.ps1        # checks for Python and the .NET SDK, offers to install
.\scripts\build-windows.ps1
```

`install-deps.ps1` is optional — the build tells you what is missing anyway — but it
saves a round trip. It never installs anything without asking; `-Yes` skips the prompt
and `-CheckOnly` reports without installing.

The build sets up the engine's Python environment the first time. To do only that step —
to run the command-line tool without building an app — use `.\scripts\setup-engine.ps1`.

Three things come out, in `build\windows\`:

| | |
|---|---|
| `win-x64\` | The app as a folder. Self-contained, copy it anywhere, run `Pcci.exe`. |
| `PCCI-win-x64.zip` | The same folder, zipped, for handing to somebody. |
| `PCCI-win-x64.msi` | An installer: per-user, into `%LOCALAPPDATA%\Programs\PCCI`, with a Start menu shortcut and an entry in Apps and Features. No administrator needed. |

`-NoInstaller` skips the .msi if you only want the portable build.

Requirements: Windows 10 1809 or later, the .NET 8 SDK, and **Python 3.12 or newer**
(`winget install Python.Python.3.12`). For an ARM machine:

```powershell
.\scripts\build-windows.ps1 -Architecture win-arm64
```

### Building for the other architecture

An Intel machine and an ARM machine need different builds. You can make either from
either, as long as the matching Python is installed:

```powershell
.\scripts\build-windows.ps1 -Architecture win-x64      # for an Intel machine
.\scripts\build-windows.ps1 -Architecture win-arm64    # for an ARM machine
```

The engine is frozen by whichever interpreter builds it, so switching architecture
rebuilds `core\.venv` around a matching one. If there is no matching Python installed
the build says so and carries on with what there is — the result still runs, under
emulation.

To build both, plus the Mac app, without owning both machines, see
`.\scripts\build-all.ps1` in the README: it runs each build on a GitHub runner and
downloads the results.

On an ARM64 machine, install the ARM64 build of Python. The engine is frozen with
whichever interpreter builds it, so an x64 Python produces an x64 engine that then runs
under emulation inside an ARM64 app. The build picks a matching Python when the machine
has more than one, and says so on screen when it cannot.

**No C++ or Rust toolchain is needed.** Every runtime dependency ships a Windows ARM64
wheel, and CI fails if one ever stops doing so. The test and lint tooling is a different
matter — `grpcio-tools` has no ARM64 wheel at all — so it is not installed unless you
ask for it:

```powershell
.\scripts\setup-engine.ps1 -Dev      # pytest, mypy, ruff; x64 only
```

## First launch

Windows will show **"Windows protected your PC"**. Click **More info**, then **Run
anyway**. Once only.

If the zip came from a browser or email, Windows may also block the files inside it.
Right-click the zip → **Properties** → tick **Unblock** → **OK**, then extract it.

## If the build fails

**`py.exe : No suitable Python runtime found`.** A checkout from before this was fixed.
The old script asked the launcher for `py -3.12`, which does not match an ARM64 install
— those register as `3.12-arm64`. `git pull` and run it again: setup now asks the
launcher what it actually has, with `py -0p`, and also looks through PATH and the usual
install folders.

**`dotnet not found`.** Install the .NET 8 SDK:
`winget install Microsoft.DotNet.SDK.8`.

**`Microsoft Visual C++ 14.0 or greater is required`**, from a wheel build for
`grpcio`, `cryptography` or similar. A checkout from before this was fixed: setup used
to install the test tooling along with the engine, and some of it has no ARM64 wheel and
had to be compiled. `git pull` and run it again. If you deliberately asked for `-Dev` on
an ARM64 machine, that is the one case where the toolchain really is needed; leave the
switch off unless you are running the tests.

**`core\.venv runs a ... Python`.** The environment was built by an interpreter of a
different architecture than the app. Harmless, but to fix it delete `core\.venv` and
build again.

## What is inside

```
Pcci.exe            the app
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
