@echo off
setlocal

REM Build a single-file Windows executable using PyInstaller.
REM Run this in a Windows terminal from repo root.

if not exist .venv (
  py -3 -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller==6.10.0

pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --name subtitle-tool ^
  --add-data "app\static;app\static" ^
  --hidden-import uvicorn.logging ^
  --hidden-import uvicorn.loops ^
  --hidden-import uvicorn.loops.auto ^
  --hidden-import uvicorn.protocols ^
  --hidden-import uvicorn.protocols.http ^
  --hidden-import uvicorn.protocols.http.auto ^
  --hidden-import uvicorn.protocols.websockets ^
  --hidden-import uvicorn.protocols.websockets.auto ^
  scripts\run_app.py

echo.
echo Build completed. EXE path: dist\subtitle-tool.exe
echo Run: dist\subtitle-tool.exe
endlocal
