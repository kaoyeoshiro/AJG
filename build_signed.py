# Script para compilar executável com configurações anti-vírus
import os
import subprocess
import sys

def build_exe_optimized():
    """
    Compila o executável com configurações otimizadas para evitar detecção como vírus
    """

    # Comando PyInstaller otimizado
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",  # Remove console (menos suspeito)
        "--name=RelatorioTJMS",
        "--icon=icon.ico",  # Se tiver ícone
        "--add-data=templates;templates",
        "--add-data=config.py;.",
        "--exclude-module=PIL",  # Excluir módulos desnecessários
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        "--strip",  # Remove símbolos de debug
        "--noupx",  # Não comprimir (UPX é suspeito)
        "main_exe.py"
    ]

    print("Compilando executável otimizado...")
    print("Comando:", " ".join(cmd))

    try:
        subprocess.run(cmd, check=True)
        print("✓ Executável compilado com sucesso!")
        print("📁 Localização: dist/RelatorioTJMS.exe")
        print("\n⚠️  Para evitar detecção como vírus:")
        print("1. NÃO comprima o arquivo .exe")
        print("2. Adicione exceção no Windows Defender")
        print("3. Considere assinatura digital para distribuição")

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na compilação: {e}")
        return False

    return True

if __name__ == "__main__":
    build_exe_optimized()