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

:: Delete existing version.txt if it exists
if exist version.txt del /f /q version.txt

:: Convert version string to tuple format
set filever=%part1%,%part2%,%part3%,%part4%

:: Create version.txt
echo # UTF-8 > version.txt
echo VSVersionInfo^( >> version.txt
echo   ffi=FixedFileInfo^( >> version.txt
echo     filevers=(%filever%), >> version.txt
echo     prodvers=(%filever%), >> version.txt
echo     mask=0x3f, >> version.txt
echo     flags=0x0, >> version.txt
echo     OS=0x4, >> version.txt
echo     fileType=0x1, >> version.txt
echo     subtype=0x0, >> version.txt
echo     date=(0,0)^ >> version.txt
echo     ), >> version.txt
echo   kids=^[ >> version.txt
echo     StringFileInfo^( >> version.txt
echo       ^[ >> version.txt
echo       StringTable^( >> version.txt
echo         '040904B0', >> version.txt
echo         ^[ >> version.txt
echo         StringStruct('CompanyName', 'Tinifan'), >> version.txt
echo         StringStruct('FileDescription', 'Inazuma Eleven Condition Compiler ^& Decompiler'), >> version.txt
echo         StringStruct('FileVersion', '%version%'), >> version.txt
echo         StringStruct('InternalName', 'inz_cond'), >> version.txt
echo         StringStruct('LegalCopyright', 'Copyright ^© Tinifan %year%'), >> version.txt
echo         StringStruct('OriginalFilename', 'inz_cond_gui.exe'), >> version.txt
echo         StringStruct('ProductName', 'inz_cond'), >> version.txt
echo         StringStruct('ProductVersion', '%version%')^] >> version.txt
echo       )^] >> version.txt
echo       ), >> version.txt
echo     VarFileInfo^([VarStruct('Translation', [1033, 1200])])^ >> version.txt
echo   ]^ >> version.txt
echo ^) >> version.txt

:: Run PyInstaller to build the executable
pyinstaller --onefile --windowed --version-file=version.txt inz_cond_gui.py

pause