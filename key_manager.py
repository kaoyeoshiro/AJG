# key_manager.py
# -*- coding: utf-8 -*-
"""
Gerenciador de chaves API para o RelatorioTJMS
Salva a chave localmente de forma segura e pede ao usuário quando necessário
"""

import os
import sys
import json
import base64
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
from typing import Optional

class KeyManager:
    def __init__(self):
        self.key_file = self._get_key_file_path()
        self.current_key = None

    def _get_key_file_path(self) -> Path:
        """Define onde salvar a chave (pasta do usuário ou executável)"""
        if getattr(sys, 'frozen', False):
            # Se for executável, salva na pasta do executável
            app_dir = Path(sys.executable).parent
        else:
            # Se for desenvolvimento, salva na pasta do projeto
            app_dir = Path(__file__).parent

        return app_dir / ".relatorio_config"

    def _encode_key(self, key: str) -> str:
        """Codifica a chave (simples obfuscação, não é criptografia real)"""
        return base64.b64encode(key.encode('utf-8')).decode('utf-8')

    def _decode_key(self, encoded_key: str) -> str:
        """Decodifica a chave"""
        try:
            return base64.b64decode(encoded_key.encode('utf-8')).decode('utf-8')
        except:
            return ""

    def save_key(self, api_key: str) -> bool:
        """Salva a chave API no arquivo local"""
        try:
            config = {
                "api_key": self._encode_key(api_key),
                "version": "1.0"
            }

            with open(self.key_file, 'w', encoding='utf-8') as f:
                json.dump(config, f)

            self.current_key = api_key
            return True
        except Exception as e:
            print(f"Erro ao salvar chave: {e}")
            return False

    def load_key(self) -> Optional[str]:
        """Carrega a chave API do arquivo local"""
        try:
            if not self.key_file.exists():
                return None

            with open(self.key_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            encoded_key = config.get("api_key", "")
            if encoded_key:
                self.current_key = self._decode_key(encoded_key)
                return self.current_key

        except Exception as e:
            print(f"Erro ao carregar chave: {e}")

        return None

    def delete_key(self) -> bool:
        """Remove a chave salva (para reconfiguração)"""
        try:
            if self.key_file.exists():
                self.key_file.unlink()
            self.current_key = None
            return True
        except Exception as e:
            print(f"Erro ao deletar chave: {e}")
            return False

    def validate_key_format(self, key: str) -> bool:
        """Valida se a chave tem o formato correto"""
        return key and key.startswith("sk-or-v1-") and len(key) > 20

    def test_key_with_api(self, key: str) -> tuple[bool, str]:
        """Testa se a chave funciona com a API OpenRouter"""
        try:
            import requests

            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }

            # Teste simples - lista de modelos
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                return True, "Chave válida"
            elif response.status_code == 401:
                return False, "Chave inválida ou expirada"
            else:
                return False, f"Erro na API: {response.status_code}"

        except requests.RequestException as e:
            return False, f"Erro de conexão: {e}"
        except Exception as e:
            return False, f"Erro inesperado: {e}"

class KeySetupDialog:
    def __init__(self, parent=None, title="Configuração Inicial", message=None):
        self.parent = parent
        self.result = None
        self.title = title
        self.message = message or "Configure sua chave OpenRouter para continuar"

    def show_setup_dialog(self) -> Optional[str]:
        """Mostra dialog para configurar chave API"""
        root = self.parent or tk.Tk()

        if not self.parent:
            root.withdraw()  # Esconde janela principal se criamos uma

        # Dialog customizado
        dialog = tk.Toplevel(root)
        dialog.title(self.title)
        dialog.geometry("500x350")
        dialog.resizable(False, False)
        dialog.transient(root)
        dialog.grab_set()

        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Conteúdo
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = tk.Label(
            main_frame,
            text="🔑 Configuração da Chave OpenRouter",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 15))

        # Mensagem
        msg_label = tk.Label(
            main_frame,
            text=self.message,
            wraplength=450,
            justify=tk.LEFT
        )
        msg_label.pack(pady=(0, 15))

        # Instruções
        instructions = """Como obter sua chave:
1. Acesse: https://openrouter.ai/keys
2. Faça login ou crie uma conta
3. Clique em "Create Key"
4. Copie a chave (sk-or-v1-...)
5. Cole abaixo:"""

        instr_label = tk.Label(
            main_frame,
            text=instructions,
            justify=tk.LEFT,
            bg="#f0f0f0",
            relief=tk.SUNKEN,
            padx=10,
            pady=10
        )
        instr_label.pack(fill=tk.X, pady=(0, 15))

        # Campo de entrada
        tk.Label(main_frame, text="Chave OpenRouter:").pack(anchor=tk.W)

        key_var = tk.StringVar()
        key_entry = tk.Entry(
            main_frame,
            textvariable=key_var,
            width=60,
            show="*"  # Oculta a chave
        )
        key_entry.pack(fill=tk.X, pady=(5, 15))
        key_entry.focus()

        # Checkbox para mostrar chave
        show_var = tk.BooleanVar()
        def toggle_show():
            key_entry.config(show="" if show_var.get() else "*")

        show_check = tk.Checkbutton(
            main_frame,
            text="Mostrar chave",
            variable=show_var,
            command=toggle_show
        )
        show_check.pack(anchor=tk.W, pady=(0, 15))

        # Status
        status_var = tk.StringVar()
        status_label = tk.Label(
            main_frame,
            textvariable=status_var,
            fg="blue"
        )
        status_label.pack(pady=(0, 15))

        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        def on_ok():
            key = key_var.get().strip()

            if not key:
                status_var.set("Por favor, insira uma chave")
                status_label.config(fg="red")
                return

            # Validação de formato
            if not key.startswith("sk-or-v1-"):
                status_var.set("Formato inválido. A chave deve começar com 'sk-or-v1-'")
                status_label.config(fg="red")
                return

            # Teste com API
            status_var.set("Testando chave...")
            status_label.config(fg="blue")
            dialog.update()

            km = KeyManager()
            valid, message = km.test_key_with_api(key)

            if valid:
                status_var.set("✓ Chave válida! Salvando...")
                status_label.config(fg="green")
                dialog.update()

                if km.save_key(key):
                    self.result = key
                    dialog.destroy()
                else:
                    status_var.set("Erro ao salvar chave")
                    status_label.config(fg="red")
            else:
                status_var.set(f"✗ {message}")
                status_label.config(fg="red")

        def on_cancel():
            self.result = None
            dialog.destroy()

        tk.Button(
            button_frame,
            text="Cancelar",
            command=on_cancel,
            width=12
        ).pack(side=tk.RIGHT, padx=(5, 0))

        tk.Button(
            button_frame,
            text="Salvar",
            command=on_ok,
            width=12,
            bg="#4CAF50",
            fg="white"
        ).pack(side=tk.RIGHT)

        # Enter para confirmar
        dialog.bind('<Return>', lambda e: on_ok())

        # Aguarda fechamento
        dialog.wait_window()

        if not self.parent:
            root.destroy()

        return self.result

def get_api_key(parent=None, force_new=False) -> Optional[str]:
    """
    Função principal para obter chave API
    - Carrega chave salva se existir
    - Mostra dialog se não tiver ou se force_new=True
    """
    km = KeyManager()

    # Se não é para forçar nova chave, tenta carregar existente
    if not force_new:
        existing_key = km.load_key()
        if existing_key:
            return existing_key

    # Mostra dialog para configurar
    message = "Configure sua chave OpenRouter para continuar usando o sistema." if not force_new else "Insira uma nova chave OpenRouter:"

    dialog = KeySetupDialog(
        parent=parent,
        title="Configuração da Chave API" if not force_new else "Reconfigurar Chave API",
        message=message
    )

    return dialog.show_setup_dialog()

if __name__ == "__main__":
    # Teste standalone
    key = get_api_key()
    if key:
        print(f"Chave configurada: {key[:20]}...")
    else:
        print("Configuração cancelada")