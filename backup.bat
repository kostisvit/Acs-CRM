@echo off
setlocal EnableDelayedExpansion

REM === Load .env file ===

set "ENV_FILE=C:\Users\KostasVit\Desktop\Projects\Acs-CRM\.env"

if not exist "%ENV_FILE%" (
    echo .env file not found: %ENV_FILE%
    exit /b 1
)

for /f "usebackq tokens=1,* delims==" %%a in ("%ENV_FILE%") do (
    set "key=%%a"
    set "value=%%b"

    if "!key!"=="DATABASE_CONTAINER" set "CONTAINER=!value!"
    if "!key!"=="DB_USER" set "DB_USER=!value!"
    if "!key!"=="DB_NAME" set "DB_NAME=!value!"
    if "!key!"=="BACKUP_DIR" set "BACKUP_DIR=!value!"
)

REM === Validate required variables ===

if not defined CONTAINER (
    echo DATABASE_CONTAINER is not defined in .env
    exit /b 1
)

if not defined DB_USER (
    echo DB_USER is not defined in .env
    exit /b 1
)

if not defined DB_NAME (
    echo DB_NAME is not defined in .env
    exit /b 1
)

if not defined BACKUP_DIR (
    echo BACKUP_DIR is not defined in .env
    exit /b 1
)

REM === Create backup directory if needed ===

if not exist "%BACKUP_DIR%" (
    mkdir "%BACKUP_DIR%"

    if errorlevel 1 (
        echo Failed to create backup directory: %BACKUP_DIR%
        exit /b 1
    )
)

REM === Generate timestamp (YYYYMMDD_HHMMSS) ===

for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do (
    set "TIMESTAMP=%%a"
)

if not defined TIMESTAMP (
    echo Failed to generate timestamp.
    exit /b 1
)

REM === Backup file path ===

set "BACKUP_FILE=%BACKUP_DIR%\%DB_NAME%_%TIMESTAMP%.sql"

echo.
echo CONTAINER=[%CONTAINER%]
echo DB_USER=[%DB_USER%]
echo DB_NAME=[%DB_NAME%]
echo BACKUP_DIR=[%BACKUP_DIR%]
echo.
echo Creating database backup:
echo %BACKUP_FILE%
echo.

REM === Run PostgreSQL backup ===

docker exec -t "%CONTAINER%" pg_dump -c -U "%DB_USER%" "%DB_NAME%" > "%BACKUP_FILE%"

if errorlevel 1 (
    echo.
    echo Backup failed!
    echo.

    if exist "%BACKUP_FILE%" del "%BACKUP_FILE%"

    exit /b 1
)

echo.
echo Backup completed successfully:
echo %BACKUP_FILE%
echo.

endlocal

