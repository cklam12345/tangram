@echo off
REM Tangram Challenge - Build Windows Executables
REM Run this file to create .exe files

echo ========================================
echo TANGRAM CHALLENGE - BUILD EXECUTABLES
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -m pip install --upgrade pip
python -m pip install pyinstaller opencv-python numpy pygame

echo.
echo [2/3] Building executables...
python build_windows_exe.py

echo.
echo [3/3] Creating portable package...
if not exist "portable_package" mkdir portable_package
xcopy /Y dist\*.exe portable_package\
xcopy /Y README.md portable_package\
xcopy /Y QUICK_REFERENCE.md portable_package\
xcopy /Y SETUP_GUIDE.md portable_package\
if exist tangram_icon.ico xcopy /Y tangram_icon.ico portable_package\

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Your executables are ready:
echo   - dist\TangramLauncher.exe (double-click to start)
echo   - portable_package\ (folder ready to share/demo)
echo.
echo For installer creation:
echo   1. Install Inno Setup from https://jrsoftware.org/isinfo.php
echo   2. Compile tangram_installer.iss
echo.
pause
