@echo off
setlocal enabledelayedexpansion

REM === Load .env file ===
set ENV_FILE=C:\Users\KostasVit\Desktop\Projects\Acs-CRM\.env
if not exist "%ENV_FILE%" (
    echo ❌ .env file not found: %ENV_FILE%
    exit /b 1
)

for /f "usebackq tokens=1,2 delims==" %%a in ("%ENV_FILE%") do (
    set "key=%%a"
    set "value=%%b"
    if "!key!"=="DATABASE_CONTAINER" set CONTAINER=!value!
    if "!key!"=="DB_USER" set DB_USER=!value!
    if "!key!"=="DB_NAME" set DB_NAME=!value!
    if "!key!"=="BACKUP_DIR" set BACKUP_DIR=!value!
)

REM === Create backup directory if needed ===
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM === Generate timestamp (YYYYMMDD_HHMM) ===
for /f "tokens=2 delims==" %%a in ('"wmic os get localdatetime /value"') do set ldt=%%a
set TIMESTAMP=%ldt:~0,8%_%ldt:~8,4%

REM === Backup file path ===
set BACKUP_FILE=%BACKUP_DIR%\%DB_NAME%_%TIMESTAMP%.sql


echo CONTAINER=[%CONTAINER%]
echo DB_USER=[%DB_USER%]
echo DB_NAME=[%DB_NAME%]
echo BACKUP_DIR=[%BACKUP_DIR%]

echo Creating database backup: %BACKUP_FILE%
docker exec -t %CONTAINER% pg_dump -c -U %DB_USER% %DB_NAME% > "%BACKUP_FILE%"

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Backup failed!
    exit /b 1
)

echo ✅ Backup completed successfully: %BACKUP_FILE%
