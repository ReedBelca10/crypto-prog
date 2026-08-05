;This SED file creates an IExpress self-extracting installer
[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=CreatePackage
ShowInstallProgramWindow=0
HideExtract=1
CreateNewCab=1
CabName=CryptoProgInstaller.cab
GenerateSetupProgram=1
SetupProgram=CryptoProg.exe
SourceFiles=0
TargetName=CryptoProg-Installer.exe
TargetPath=%TEMP%
FileCount=1
[Strings]
InstallProgram=CryptoProg.exe
