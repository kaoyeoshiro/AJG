# cleanup_workflows.py
# -*- coding: utf-8 -*-
"""
Script para limpar workflows antigos do GitHub Actions
Mantém apenas os últimos N workflows bem-sucedidos
"""

import subprocess
import json
import sys

def run_gh_command(cmd):
    """Executa comando do GitHub CLI"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return None

def get_workflow_runs(repo, limit=50):
    """Obtém lista de workflow runs"""
    cmd = f'gh run list --repo {repo} --limit {limit} --json databaseId,conclusion,workflowName,createdAt'
    output = run_gh_command(cmd)

    if output:
        try:
            return json.loads(output)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return []
    return []

def cleanup_workflows(repo="kaoyeoshiro/AJG", keep_count=5):
    """
    Limpa workflows antigos, mantendo apenas os últimos keep_count

    Args:
        repo: Nome do repositório
        keep_count: Número de workflows para manter
    """
    print(f"Limpando workflows do repositório {repo}")
    print(f"Mantendo os últimos {keep_count} workflows...")

    # Obter todos os workflows
    runs = get_workflow_runs(repo)

    if not runs:
        print("Nenhum workflow encontrado ou erro ao obter lista")
        return

    print(f"Total de workflows encontrados: {len(runs)}")

    # Separar por status
    successful_runs = [r for r in runs if r['conclusion'] == 'success']
    failed_runs = [r for r in runs if r['conclusion'] == 'failure']
    other_runs = [r for r in runs if r['conclusion'] not in ['success', 'failure']]

    print(f"Bem-sucedidos: {len(successful_runs)}")
    print(f"Falhados: {len(failed_runs)}")
    print(f"Outros: {len(other_runs)}")

    # Deletar todos os falhados
    deleted_count = 0
    if failed_runs:
        print("\nDeletando workflows falhados...")
        for run in failed_runs:
            cmd = f'gh run delete {run["databaseId"]} --repo {repo}'
            if run_gh_command(cmd):
                print(f"  ✓ Deletado: {run['databaseId']}")
                deleted_count += 1
            else:
                print(f"  ✗ Falha ao deletar: {run['databaseId']}")

    # Manter apenas os últimos N bem-sucedidos
    if len(successful_runs) > keep_count:
        to_delete = successful_runs[keep_count:]
        print(f"\nDeletando {len(to_delete)} workflows bem-sucedidos antigos...")

        for run in to_delete:
            cmd = f'gh run delete {run["databaseId"]} --repo {repo}'
            if run_gh_command(cmd):
                print(f"  ✓ Deletado: {run['databaseId']} - {run['createdAt']}")
                deleted_count += 1
            else:
                print(f"  ✗ Falha ao deletar: {run['databaseId']}")

    print(f"\n✅ Limpeza concluída! {deleted_count} workflows deletados.")
    print(f"Workflows restantes: {len(runs) - deleted_count}")

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        keep_count = int(sys.argv[1])
    else:
        keep_count = 5

    print("GitHub Actions Workflow Cleanup")
    print("=" * 40)

    cleanup_workflows(keep_count=keep_count)

if __name__ == "__main__":
    main()