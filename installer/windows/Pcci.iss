; The Windows installer.
;
; Built by scripts/build-installer.ps1, which passes in the folder to package and where
; to write the result. Everything in that folder ships, so it must be a finished build:
; the app, the frozen engine beside it, and nothing else.
;
; What it offers, and why each one is here rather than assumed:
;
;   * Install for all users or just me, asked on the first page. "All users" needs
;     administrator and puts it in Program Files; "just me" needs nothing and goes to
;     the user's own folder.
;   * Any folder at all, on the directory page. The default follows the choice above.
;   * A desktop shortcut, optional. {autodesktop} resolves to the *public* desktop for
;     an all-users install, so everyone who signs in sees it, and to the installing
;     user's own desktop otherwise. That is the whole reason the icon uses {auto...}
;     constants rather than naming a folder.
;
; There is no code-signing certificate for this project, so SmartScreen warns on first
; run. See docs/INSTALL_WINDOWS.md.

#ifndef SourceFolder
  #error SourceFolder must be passed in: ISCC /DSourceFolder=...
#endif
#ifndef OutputDir
  #error OutputDir must be passed in: ISCC /DOutputDir=...
#endif
#ifndef OutputName
  #define OutputName "PCCI-setup"
#endif
#ifndef AppVersion
  #define AppVersion "0.3.0"
#endif
#ifndef Arch
  #define Arch "x64"
#endif

#define AppName "ProPresenter Chord Chart Importer"
#define ShortName "PCCI"
#define AppExe "Pcci.exe"

[Setup]
; Shared between the x64 and ARM64 builds on purpose: installing one replaces the
; other rather than leaving two copies behind.
AppId={{96deb8d7-f44b-41bf-bf03-ea801fccac72}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=PCCI
AppSupportURL=https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer
DefaultDirName={autopf}\{#ShortName}
DefaultGroupName={#ShortName}
DisableProgramGroupPage=yes
DisableDirPage=no
AllowNoIcons=yes

; Start without administrator and let the first page ask. Requiring elevation up front
; would mean an unsigned installer demanding administrator before it has said what it
; is for.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog commandline

OutputDir={#OutputDir}
OutputBaseFilename={#OutputName}
SetupIconFile={#SourceFolder}\Assets\AppIcon.ico
UninstallDisplayIcon={app}\{#AppExe}
UninstallDisplayName={#AppName}
WizardStyle=modern
Compression=lzma2/max
SolidCompression=yes
#if Arch == "arm64"
ArchitecturesAllowed=arm64
ArchitecturesInstallIn64BitMode=arm64
#else
ArchitecturesInstallIn64BitMode=x64
#endif

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
  GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#SourceFolder}\*"; DestDir: "{app}"; \
  Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExe}"
; {autodesktop} is the public desktop for an all-users install and the user's own
; desktop otherwise, which is exactly the behaviour wanted here.
Name: "{autodesktop}\{#ShortName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#ShortName}}"; \
  Flags: nowait postinstall skipifsilent
