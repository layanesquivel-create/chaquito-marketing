@echo off
cd /d D:\chaquito-marketing

echo [INICIO] %date% %time% - Ejecutando pipeline diario de marketing Chaquito >> logs\ejecucion_diaria.log
python main.py >> logs\ejecucion_diaria.log 2>&1
if %errorlevel%==0 (
    echo [OK] %date% %time% - Pipeline completado exitosamente >> logs\ejecucion_diaria.log
) else (
    echo [ERROR] %date% %time% - Pipeline fallo con codigo %errorlevel% >> logs\ejecucion_diaria.log
)
echo ---------------------------------------- >> logs\ejecucion_diaria.log
