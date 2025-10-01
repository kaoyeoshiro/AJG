# Script PowerShell para adicionar exceção no Windows Defender
# Execute como Administrador

param(
    [string]$ExecutablePath = ".\dist\RelatorioTJMS.exe",
    [string]$ProjectFolder = "."
)

Write-Host "🛡️  Configurando exceções no Windows Defender..." -ForegroundColor Green

# Obter caminhos absolutos
$ExePath = Resolve-Path $ExecutablePath -ErrorAction SilentlyContinue
$ProjectPath = Resolve-Path $ProjectFolder

# Adicionar exceção para o executável
if ($ExePath) {
    try {
        Add-MpPreference -ExclusionPath $ExePath.Path
        Write-Host "✓ Exceção adicionada para: $($ExePath.Path)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Erro ao adicionar exceção para o executável: $_" -ForegroundColor Red
    }
}

# Adicionar exceção para a pasta do projeto
try {
    Add-MpPreference -ExclusionPath $ProjectPath.Path
    Write-Host "✓ Exceção adicionada para pasta: $($ProjectPath.Path)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro ao adicionar exceção para a pasta: $_" -ForegroundColor Red
}

# Adicionar exceção para processo PyInstaller
try {
    Add-MpPreference -ExclusionProcess "python.exe"
    Add-MpPreference -ExclusionProcess "pyinstaller.exe"
    Write-Host "✓ Exceções adicionadas para processos Python/PyInstaller" -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro ao adicionar exceções de processo: $_" -ForegroundColor Red
}

Write-Host "`n📋 Para verificar as exceções ativas:" -ForegroundColor Yellow
Write-Host "Get-MpPreference | Select-Object -ExpandProperty ExclusionPath" -ForegroundColor Gray

Write-Host "`n⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "- Execute este script como Administrador" -ForegroundColor Gray
Write-Host "- As exceções são permanentes até serem removidas manualmente" -ForegroundColor Gray
Write-Host "- Recompile o executável usando build_signed.py" -ForegroundColor Gray