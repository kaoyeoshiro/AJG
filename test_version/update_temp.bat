@echo off
echo Aplicando atualiza��o...
timeout /t 2 /nobreak > nul
move /y "C:\Users\kaoye\AppData\Local\Temp\RelatorioTJMS_update_v1.0.17.exe" "RelatorioTJMS.exe"
echo v1.0.17 > VERSION
echo Atualiza��o conclu�da!
start "" "RelatorioTJMS.exe"
del "%~f0"
