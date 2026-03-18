@echo off
REM Cyber Runner Windows Build Script
REM Run this on Windows to create .exe files

echo [BUILDER] Starting Windows build...

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM Install PyInstaller
echo [BUILDER] Installing PyInstaller...
python -m pip install pyinstaller

REM Build game executable
echo [BUILDER] Building Cyber Runner game...
pyinstaller --onefile --windowed --name CyberRunner --add-data "README.md;." main.py

REM Build cleaner executable
echo [BUILDER] Building Cyber Runner Cleaner...
pyinstaller --onefile --console --name CyberRunnerCleaner cleanup.py

REM Create release package
echo [BUILDER] Creating release package...
if not exist release mkdir release
copy dist\*.exe release\
copy README.md release\

echo # Cyber Runner - Windows Executable Package > release\USAGE.txt
echo. >> release\USAGE.txt
echo ## Files Included: >> release\USAGE.txt
echo - CyberRunner.exe - Main game executable >> release\USAGE.txt
echo - CyberRunnerCleaner.exe - Cleanup utility >> release\USAGE.txt
echo - README.md - Complete documentation >> release\USAGE.txt
echo. >> release\USAGE.txt
echo ## Quick Start: >> release\USAGE.txt
echo 1. Run CyberRunner.exe >> release\USAGE.txt
echo 2. Follow the on-screen instructions >> release\USAGE.txt
echo 3. Use CyberRunnerCleaner when done >> release\USAGE.txt
echo. >> release\USAGE.txt
echo ## System Requirements: >> release\USAGE.txt
echo - Windows operating system >> release\USAGE.txt
echo - No additional dependencies required >> release\USAGE.txt
echo. >> release\USAGE.txt
echo ## For Educational Use Only! >> release\USAGE.txt
echo Run only in controlled virtual machine environments. >> release\USAGE.txt

echo.
echo [BUILDER] Windows build completed!
echo [BUILDER] Executables available in: dist\
echo [BUILDER] Release package in: release\
pause
