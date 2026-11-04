@echo off
REM One-click render for Windows. Double-click or run from the project folder.
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is not installed. Install the LTS version from https://nodejs.org and run this again.
  pause
  exit /b 1
)
if not exist node_modules (
  echo Installing dependencies - first run only...
  call npm install
  if errorlevel 1 ( echo npm install failed & pause & exit /b 1 )
)
echo Rendering video...
call npx remotion render src/index.ts Main out/video.mp4
if errorlevel 1 ( echo Render failed - see README-RENDER.md troubleshooting & pause & exit /b 1 )
echo Done: out\video.mp4
pause
