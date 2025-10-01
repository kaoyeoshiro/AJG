#!/usr/bin/env python3
"""
Script para configurar releases seguros no GitHub
"""

import os
import subprocess
import sys

def check_requirements():
    """Verifica se os requisitos estão atendidos"""
    print("🔍 Verificando requisitos...")

    # Verificar se está em um repositório Git
    try:
        subprocess.run(["git", "status"], check=True, capture_output=True)
        print("✅ Repositório Git detectado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Este não é um repositório Git ou Git não está instalado")
        return False

    # Verificar se tem origin remoto
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"],
                              check=True, capture_output=True, text=True)
        origin = result.stdout.strip()
        if "github.com" in origin:
            print(f"✅ GitHub origin detectado: {origin}")
        else:
            print(f"⚠️ Origin não é do GitHub: {origin}")
    except subprocess.CalledProcessError:
        print("❌ Remote 'origin' não configurado")
        return False

    # Verificar arquivos necessários
    required_files = [
        "main_exe.py",
        "config.py",
        "requirements.txt",
        "RelatorioTJMS.spec"
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} encontrado")
        else:
            print(f"❌ {file} não encontrado")
            return False

    return True

def setup_workflow():
    """Configura o workflow do GitHub Actions"""
    print("\n🔧 Configurando workflow GitHub Actions...")

    # Criar diretório se não existir
    workflow_dir = ".github/workflows"
    os.makedirs(workflow_dir, exist_ok=True)

    workflow_file = os.path.join(workflow_dir, "build-release.yml")
    if os.path.exists(workflow_file):
        print(f"✅ Workflow já existe: {workflow_file}")
    else:
        print(f"❌ Workflow não encontrado: {workflow_file}")
        print("Execute o script de criação do workflow primeiro!")
        return False

    return True

def create_first_release():
    """Cria a primeira release/tag"""
    print("\n🏷️ Configurando primeira release...")

    # Verificar se já existe alguma tag
    try:
        result = subprocess.run(["git", "tag"], capture_output=True, text=True)
        existing_tags = result.stdout.strip().split('\n') if result.stdout.strip() else []

        if existing_tags and existing_tags[0]:
            print(f"✅ Tags existentes: {', '.join(existing_tags)}")
            return True

    except subprocess.CalledProcessError:
        pass

    # Criar primeira tag
    version = "v1.0.0"
    try:
        # Criar tag
        subprocess.run(["git", "tag", "-a", version, "-m", f"Release {version}"], check=True)
        print(f"✅ Tag {version} criada")

        # Push da tag
        confirm = input(f"\n🚀 Fazer push da tag {version} para o GitHub? (y/N): ")
        if confirm.lower() == 'y':
            subprocess.run(["git", "push", "origin", version], check=True)
            print(f"✅ Tag {version} enviada para o GitHub")
            print("\n🎉 Release será compilada automaticamente pelo GitHub Actions!")
        else:
            print("ℹ️ Para criar a release depois, execute: git push origin v1.0.0")

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar tag: {e}")
        return False

    return True

def show_next_steps():
    """Mostra os próximos passos"""
    print("\n" + "="*60)
    print("🎯 PRÓXIMOS PASSOS")
    print("="*60)

    print("\n1. 🔐 CONFIGURAR ASSINATURA DIGITAL (Opcional):")
    print("   - Obtenha um certificado de code signing")
    print("   - Configure os secrets no GitHub:")
    print("     * CERTIFICATE_BASE64")
    print("     * CERTIFICATE_PASSWORD")
    print("   - Veja CERTIFICADO_DIGITAL.md para detalhes")

    print("\n2. 📋 CONFIGURAR SECRETS NECESSÁRIOS:")
    print("   - Vá em Settings → Secrets and variables → Actions")
    print("   - Adicione OPENROUTER_API_KEY (ou mantenha placeholder)")

    print("\n3. 🚀 CRIAR RELEASES:")
    print("   - Para release manual: GitHub → Releases → Create a new release")
    print("   - Para release automática: git tag v1.0.1 && git push origin v1.0.1")

    print("\n4. 📖 DOCUMENTAR PARA USUÁRIOS:")
    print("   - Adicione DOWNLOAD_SEGURO.md ao README")
    print("   - Instrua sobre Windows Defender")
    print("   - Mencione verificação de checksums")

    print("\n5. 🔍 MONITORAR:")
    print("   - Acompanhe builds no GitHub Actions")
    print("   - Teste downloads em máquinas limpas")
    print("   - Monitore feedback dos usuários")

    print("\n" + "="*60)
    print("✅ CONFIGURAÇÃO COMPLETA!")
    print("="*60)

def main():
    print("🔒 CONFIGURADOR DE RELEASES SEGUROS")
    print("="*40)

    if not check_requirements():
        print("\n❌ Alguns requisitos não foram atendidos.")
        print("Corrija os problemas e execute novamente.")
        sys.exit(1)

    if not setup_workflow():
        print("\n❌ Falha na configuração do workflow.")
        sys.exit(1)

    if not create_first_release():
        print("\n❌ Falha na criação da primeira release.")
        sys.exit(1)

    show_next_steps()

if __name__ == "__main__":
    main()