# updater.py
# -*- coding: utf-8 -*-
"""
Módulo de auto-atualização para o RelatorioTJMS
Verifica releases no GitHub e baixa novas versões automaticamente
"""

import os
import sys
import json
import requests
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import tkinter as tk
from tkinter import messagebox

# Configurações do repositório
REPO_OWNER = "kaoyeoshiro"
REPO_NAME = "AJG"
CURRENT_VERSION_FILE = "VERSION"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

class AutoUpdater:
    def __init__(self, current_version: str = None):
        self.current_version = current_version or self._get_current_version()
        self.session = requests.Session()

    def _get_current_version(self) -> str:
        """Obtém a versão atual do arquivo VERSION ou retorna padrão"""
        try:
            if os.path.exists(CURRENT_VERSION_FILE):
                with open(CURRENT_VERSION_FILE, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except:
            pass
        return "v1.0.0"

    def check_for_updates(self) -> Optional[Dict[Any, Any]]:
        """Verifica se há uma nova versão disponível"""
        try:
            response = self.session.get(f"{GITHUB_API_URL}/releases/latest", timeout=10)
            response.raise_for_status()

            release_data = response.json()
            latest_version = release_data.get("tag_name", "")

            if self._is_newer_version(latest_version, self.current_version):
                return {
                    "version": latest_version,
                    "name": release_data.get("name", ""),
                    "body": release_data.get("body", ""),
                    "assets": release_data.get("assets", []),
                    "html_url": release_data.get("html_url", "")
                }
        except Exception as e:
            print(f"Erro ao verificar atualizações: {e}")
            return None

        return None

    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Compara versões (formato: v1.2.3)"""
        try:
            # Remove 'v' do início e converte para números
            latest_nums = [int(x) for x in latest.lstrip('v').split('.')]
            current_nums = [int(x) for x in current.lstrip('v').split('.')]

            # Normaliza o tamanho das listas
            max_len = max(len(latest_nums), len(current_nums))
            latest_nums.extend([0] * (max_len - len(latest_nums)))
            current_nums.extend([0] * (max_len - len(current_nums)))

            return latest_nums > current_nums
        except:
            return latest != current

    def download_update(self, release_data: Dict[Any, Any], progress_callback=None) -> Optional[str]:
        """Baixa a nova versão do executável"""
        try:
            # Procura pelo executável nos assets
            exe_asset = None
            for asset in release_data.get("assets", []):
                if asset["name"].endswith(".exe"):
                    exe_asset = asset
                    break

            if not exe_asset:
                raise Exception("Executável não encontrado no release")

            download_url = exe_asset["browser_download_url"]
            file_size = exe_asset.get("size", 0)

            # Baixa para arquivo temporário
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f"RelatorioTJMS_update_{release_data['version']}.exe")

            response = self.session.get(download_url, stream=True, timeout=30)
            response.raise_for_status()

            with open(temp_file, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and file_size > 0:
                            progress = (downloaded / file_size) * 100
                            progress_callback(progress)

            return temp_file

        except Exception as e:
            print(f"Erro ao baixar atualização: {e}")
            return None

    def apply_update(self, temp_exe_path: str, new_version: str) -> bool:
        """Aplica a atualização substituindo o executável atual"""
        try:
            current_exe = sys.executable if getattr(sys, 'frozen', False) else "RelatorioTJMS.exe"

            # Cria script batch para atualização
            batch_content = f'''@echo off
echo Aplicando atualização...
timeout /t 2 /nobreak > nul
move /y "{temp_exe_path}" "{current_exe}"
echo {new_version} > {CURRENT_VERSION_FILE}
echo Atualização concluída!
start "" "{current_exe}"
del "%~f0"
'''

            batch_file = "update_temp.bat"
            with open(batch_file, 'w', encoding='cp1252') as f:
                f.write(batch_content)

            # Executa o batch e fecha o programa
            subprocess.Popen([batch_file], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            return True

        except Exception as e:
            print(f"Erro ao aplicar atualização: {e}")
            return False

def check_and_update(parent_window=None, silent=False):
    """Função principal para verificar e aplicar atualizações"""
    updater = AutoUpdater()

    # Verifica se há atualizações
    update_info = updater.check_for_updates()

    if not update_info:
        if not silent:
            if parent_window:
                messagebox.showinfo("Atualizações", "Você já está usando a versão mais recente!", parent=parent_window)
            else:
                print("✅ Sistema atualizado - versão mais recente em uso")
        return False

    # Pergunta se deseja atualizar
    message = f"""Nova versão disponível!

Versão atual: {updater.current_version}
Nova versão: {update_info['version']}

Deseja atualizar agora?

Nota: O programa será fechado e reaberto automaticamente."""

    if parent_window:
        result = messagebox.askyesno("Atualização Disponível", message, parent=parent_window)
    else:
        print(message)
        result = input("Atualizar? (s/n): ").lower() == 's'

    if not result:
        return False

    # Progress window se tiver parent
    progress_window = None
    progress_var = None

    if parent_window:
        progress_window = tk.Toplevel(parent_window)
        progress_window.title("Baixando Atualização")
        progress_window.geometry("400x100")
        progress_window.transient(parent_window)
        progress_window.grab_set()

        tk.Label(progress_window, text="Baixando nova versão...").pack(pady=10)
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        progress_bar.pack(fill='x', padx=20, pady=10)

        def update_progress(value):
            progress_var.set(value)
            progress_window.update()

    # Baixa a atualização
    temp_file = updater.download_update(update_info, update_progress if parent_window else None)

    if progress_window:
        progress_window.destroy()

    if not temp_file:
        if parent_window:
            messagebox.showerror("Erro", "Falha ao baixar a atualização!", parent=parent_window)
        else:
            print("❌ Erro ao baixar atualização")
        return False

    # Aplica a atualização
    success = updater.apply_update(temp_file, update_info['version'])

    if success:
        if parent_window:
            messagebox.showinfo("Sucesso", "Atualização baixada! O programa será reiniciado.", parent=parent_window)
            parent_window.quit()
        else:
            print("🔄 Aplicando atualização e reiniciando...")

        # Encerra o programa (será reiniciado pelo batch)
        sys.exit(0)
    else:
        if parent_window:
            messagebox.showerror("Erro", "Falha ao aplicar a atualização!", parent=parent_window)
        else:
            print("❌ Erro ao aplicar atualização")
        return False

    return True

if __name__ == "__main__":
    # Teste standalone
    check_and_update(silent=False)