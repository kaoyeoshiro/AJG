@echo off
echo Aplicando atualização...
timeout /t 2 /nobreak > nul
move /y "C:\Users\kaoye\AppData\Local\Temp\RelatorioTJMS_update_v1.0.17.exe" "RelatorioTJMS.exe"
echo v1.0.17 > VERSION
echo Atualização concluída!
start "" "RelatorioTJMS.exe"
del "%~f0"
