```bat
@echo off
setlocal

cd /d "%~dp0"

echo ================================
echo  Setting up Python environment
echo ================================

echo Creating/updating virtual environment...
uv sync

if errorlevel 1 (
    echo uv sync failed.
    exit /b 1
)

echo.
echo Starting Python HTTP server...

start "Python HTTP Server" cmd /c "uv run python -m http.server 8000 > server.log 2>&1"

timeout /t 2 /nobreak >nul

echo HTTP server started on port 8000

echo.
echo Starting Django server...

uv run --env-file=.env python manage.py runserver --settings=config.settings.production

endlocal
```
