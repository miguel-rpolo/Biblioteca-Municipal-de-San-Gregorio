@echo off
REM ===================================
REM Biblioteca Municipal de San Gregorio
REM Ejecución completa: setup + datos + run
REM ===================================

setlocal

REM 1. Crear entorno virtual si no existe
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
)

REM 2. Activar entorno virtual
call venv\Scripts\activate.bat

REM 3. Instalar requirements si hace falta
IF NOT EXIST "venv\Lib\site-packages\flask" (
    echo [INFO] Instalando dependencias base...
    pip install -r requirements.txt
)
IF NOT EXIST "venv\Lib\site-packages\pytest" (
    echo [INFO] Instalando dependencias de desarrollo...
    pip install -r requirements-dev.txt
)

REM 4. Migrar la base de datos (crear/tocar si no existe)
IF NOT EXIST "instance\app.db" (
    echo [INFO] Migrando base de datos inicial...
    python migrate_db.py
)

REM 5. Seed de datos si está vacío
python seed_data.py

REM 6. Lanzar la aplicación
echo [INFO] Iniciando el servidor web Flask...
python run.py

endlocal
