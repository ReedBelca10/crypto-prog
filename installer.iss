[Setup]
AppName=CryptoProg
AppVersion=1.0
DefaultDirName={autopf}\CryptoProg
DefaultGroupName=CryptoProg
OutputBaseFilename=CryptoProg-Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
OutputDir=.
SetupIconFile=.
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\CryptoProg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CryptoProg"; Filename: "{app}\CryptoProg.exe"
Name: "{autodesktop}\CryptoProg"; Filename: "{app}\CryptoProg.exe"

[Run]
Filename: "{app}\CryptoProg.exe"; Description: "Launch CryptoProg"; Flags: nowait postinstall skipifsilent
