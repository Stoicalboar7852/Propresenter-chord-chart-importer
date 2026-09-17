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
| `PCCI-win-x64-setup.exe` | An installer. See below. |

`-NoInstaller` skips the setup program if you only want the portable build.

### What the installer asks

| Page | What you get |
|---|---|
| Install for | **All users** — Program Files, needs administrator, and everyone who signs in to the machine gets it. **Just me** — your own folder, no administrator, nobody else sees it. |
| Location | Whatever folder you like. The default follows the choice above: `C:\Program Files\PCCI` for all users, `%LOCALAPPDATA%\Programs\PCCI` for just you. |
| Desktop shortcut | Off by default, tick to add one. An all-users install puts it on the **public** desktop so it appears for every account; a personal install puts it on yours alone. |

It registers in Apps and Features either way, so it uninstalls like anything else, and
installing a newer build replaces the old one rather than stacking beside it.

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

## Getting a song in

Four ways, all of which end in the same review screen.

**Drop a file on the window** — Word, PDF, plain text, Markdown, RTF, OpenDocument,
HTML or ChordPro. A chart with no chords in it, such as a hymn text or a lyrics sheet,
works just as well as one with chords.

**Search for it.** Type a song name in the box at the top. Every source is asked at
once and the answers merged into one row per song, so a row can carry chords from one
site and its cover art from another; each row says which sites it came from and whether
it has chords, just the words, or nothing importable. **Import** downloads it and drops
it into the list.

**Paste a link** into the same box — a chord site, a church's own chart page, a Google
Doc published to the web, a ChordPro file in a repository. When a page lays its chart
out as preformatted text, which is where the column alignment lives, that is taken
exactly as it is.

**Paste the chart itself**, the way ProPresenter's own clipboard import works. Copy the
chart from wherever you are reading it and press **Ctrl+Shift+V**. This is also the answer
when a site refuses to let a program read it: open the page yourself, select the chart,
copy, paste.

Only Apple Music's source is a documented public API; the rest are read the way a
browser reads them, so they can change or say no without warning. Genius in particular
refuses automated requests from some networks. When a source says no, the search says
which one, carries on with the others, and suggests the clipboard — which always works.

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

**`no Inno Setup`.** The installer is built with Inno Setup, which the build installs
for you through Chocolatey or winget when it is missing. If neither is available, get it
from https://jrsoftware.org/isdl.php, or build without an installer using
`-NoInstaller`.

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
