@echo off
echo Building Spotify Bot Executable...
echo.

:: Install PyInstaller if not already installed
pip install pyinstaller

:: Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

:: Build the executable
pyinstaller --clean spotify_bot.spec

:: Check if build was successful
if exist "dist\SpotifyBot.exe" (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable created: dist\SpotifyBot.exe
    echo.
    echo You can now run the bot by double-clicking SpotifyBot.exe
    echo Make sure chromedriver.exe is in the same folder!
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo.
    echo Check the output above for errors.
    echo.
    pause
)
