@echo off
setlocal enabledelayedexpansion

:: Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller is not installed.
    echo Please install it with: pip install pyinstaller
    pause
    exit /b
)

:: Ask for the version
:ask_version
set /p version="Enter the version (format a.b.c.d) or type 'cancel' to abort: "
if /i "%version%"=="cancel" (
    echo Operation cancelled.
    exit /b
)

:: Check version format
for /f "tokens=1-4 delims=." %%a in ("%version%") do (
    set part1=%%a
    set part2=%%b
    set part3=%%c
    set part4=%%d
)

if "%part1%"=="" (
    echo Invalid version format. Example: 1.0.0.0
    goto ask_version
)
if "%part2%"=="" (
    echo Invalid version format. Example: 1.0.0.0
    goto ask_version
)
if "%part3%"=="" (
    echo Invalid version format. Example: 1.0.0.0
    goto ask_version
)
if "%part4%"=="" (
    echo Invalid version format. Example: 1.0.0.0
    goto ask_version
)

:: Get the current year from system date
for /f "tokens=3 delims=/ " %%a in ("%date%") do set year=%%a

:: Create the version.txt file
(
echo # UTF-8
echo VSVersionInfo^(
echo   ffi=FixedFileInfo^(
echo     filevers=(%version%),
echo     prodvers=(%version%),
echo     mask=0x3f,
echo     flags=0x0,
echo     OS=0x4,
echo     fileType=0x1,
echo     subtype=0x0,
echo     date=(0,0)^
echo     ),
echo   kids=^[
echo     StringFileInfo^(
echo       ^[
echo       StringTable^(
echo         '040904B0',
echo         ^[
echo         StringStruct('CompanyName', 'Tinifan'),
echo         StringStruct('FileDescription', 'Inazuma Eleven Condition Compiler & Decompiler'),
echo         StringStruct('FileVersion', '%version%'),
echo         StringStruct('InternalName', 'inz_cond'),
echo         StringStruct('LegalCopyright', 'Copyright © Tinifan %year%'),
echo         StringStruct('OriginalFilename', 'inz_cond_gui.exe'),
echo         StringStruct('ProductName', 'inz_cond'),
echo         StringStruct('ProductVersion', '%version%')^]
echo       )^]
echo       )^],
echo     VarFileInfo^([VarStruct('Translation', [1033, 1200])])^
echo   ]^
echo ^)
) > version.txt

:: Run PyInstaller to build the executable
pyinstaller --onefile --windowed --version-file=version.txt inz_cond_gui.py

pause
