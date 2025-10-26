@echo off
setlocal enabledelayedexpansion

:: Ask for the version
:ask_version
set /p version="Enter the version (format a.b.c.d) or type 'cancel' to abort: "
if /i "%version%"=="cancel" (
    echo Operation cancelled.
    exit /b
)
if "%version%"=="" (
    echo Version cannot be empty.
    goto ask_version
)

:: Create releases\<version> directory
set release_dir=%~dp0releases\%version%
if not exist "%release_dir%" mkdir "%release_dir%"

:: Create inz_cond.zip with project folders and files
echo Creating inz_cond.zip...
powershell -Command ^
    "$sourceFolders=@('gui','languages','level_5','templates','tools');" ^
    "$sourceFiles=@('inz_cond_cmd.py','inz_cond_gui.py','inz_cond_test.py','LICENSE','requirements.txt','README.md');" ^
    "$temp=New-Item -ItemType Directory -Path ([System.IO.Path]::GetTempPath() + [System.Guid]::NewGuid().ToString());" ^
    "foreach ($f in $sourceFolders) { Copy-Item $f -Destination $temp -Recurse -Force -Exclude '__pycache__' -ErrorAction SilentlyContinue };" ^
    "foreach ($f in $sourceFiles) { Copy-Item $f -Destination $temp -Force -ErrorAction SilentlyContinue };" ^
    "Compress-Archive -Path $temp\* -DestinationPath '%release_dir%\inz_cond.zip' -Force;" ^
    "Remove-Item -Recurse -Force $temp;"

:: Check if dist\inz_cond_gui.exe exists
if not exist "%~dp0dist\inz_cond_gui.exe" (
    echo Error: dist\inz_cond_gui.exe not found!
    pause
    exit /b
)

:: Create inz_cond_gui_windows.zip from dist
echo Creating inz_cond_gui_windows.zip...
powershell -Command ^
    "$temp=New-Item -ItemType Directory -Path ([System.IO.Path]::GetTempPath() + [System.Guid]::NewGuid().ToString());" ^
    "Copy-Item '%~dp0dist\inz_cond_gui.exe' -Destination $temp;" ^
    "Compress-Archive -Path $temp\* -DestinationPath '%release_dir%\inz_cond_gui_windows.zip' -Force;" ^
    "Remove-Item -Recurse -Force $temp;"

echo All done!
pause