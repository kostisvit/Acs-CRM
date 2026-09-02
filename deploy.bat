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
echo ================================
echo  Pulling latest Docker images
echo ================================

docker compose pull

if errorlevel 1 (
    echo Docker Compose pull failed.
    exit /b 1
)

echo.
echo ================================
echo  Starting Docker Compose services
echo ================================

docker compose up -d --wait

if errorlevel 1 (
    echo Docker Compose services failed to start.
    exit /b 1
)

echo Docker services are ready.

echo.
echo ================================
echo  Starting Python HTTP server
echo ================================

start "Python HTTP Server" cmd /c "uv run python -m http.server 8000 > server.log 2>&1"

timeout /t 2 /nobreak >nul

echo HTTP server started on port 8000

echo.
echo ================================
echo  Starting Django server
echo ================================

uv run --env-file=.env python manage.py migrate --settings=config.settings.production

uv run --env-file=.env python manage.py runserver 0.0.0.0:8000 --settings=config.settings.production

endlocal

