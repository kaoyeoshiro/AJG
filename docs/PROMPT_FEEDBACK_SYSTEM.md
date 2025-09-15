# 📋 PROMPT COMPLETO: Sistema de Feedback Automatizado com Google Forms

## 🎯 Contexto e Objetivo

Preciso implementar um sistema de feedback automatizado e inteligente em minha aplicação Python/Tkinter que:
1. Colete feedback de sucesso e erro automaticamente
2. Use Google Forms como backend gratuito e sem autenticação
3. Capture informações técnicas relevantes sem intervenção do usuário
4. Seja transparente mas não intrusivo
5. Funcione tanto em desenvolvimento quanto em produção (executável .exe)

## 🏗️ Arquitetura Desejada

### 1. **Google Forms como Backend**
- Criar um formulário Google com campos específicos para captura de dados
- Extrair os IDs dos campos do formulário para envio programático
- Usar requisições POST diretas sem necessidade de API Keys

### 2. **Tipos de Feedback**
O sistema deve capturar 3 tipos de eventos:

```python
FEEDBACK_TYPES = {
    "ERRO": "Erro reportado pelo usuário",
    "SUCESSO_AUTO": "Sucesso automático ao fechar",
    "PROBLEMA": "Problema identificado durante uso"
}
```

### 3. **Dados a Capturar**
- **Timestamp**: Data/hora do evento
- **Tipo de Feedback**: ERRO, SUCESSO_AUTO, PROBLEMA
- **Processo**: Identificador único da operação (ex: número do processo judicial)
- **Modelo**: Versão ou configuração usada (ex: modelo de IA)
- **Descrição**: Detalhes do problema ou sucesso
- **Informações do Sistema**: OS, versão Python, etc.
- **Stack Trace**: Em caso de erro (opcional)

## 📝 Implementação Completa

### PASSO 1: Criar o Google Form

1. Acesse https://forms.google.com
2. Crie um novo formulário com os seguintes campos:
   - **Timestamp** (Resposta curta)
   - **Tipo de Feedback** (Múltipla escolha: ERRO, SUCESSO_AUTO, PROBLEMA)
   - **Processo** (Resposta curta)
   - **Modelo** (Resposta curta)
   - **Descrição** (Parágrafo)
   - **Sistema** (Resposta curta)
   - **Erro Técnico** (Parágrafo - opcional)

3. Obtenha o link de pré-preenchimento:
   - Clique nos 3 pontos → "Obter link pré-preenchido"
   - Preencha todos os campos com valores teste
   - Copie o link gerado

### PASSO 2: Extrair IDs dos Campos

Crie este script para extrair os IDs automaticamente:

```python
# extract_form_ids.py
import re
from urllib.parse import urlparse, parse_qs

def extract_form_ids(prefilled_url):
    """
    Extrai o form_id e os field_ids de uma URL pré-preenchida do Google Forms
    """
    # Parse da URL
    parsed = urlparse(prefilled_url)
    path_parts = parsed.path.split('/')

    # Extrair form_id
    form_id = None
    for i, part in enumerate(path_parts):
        if part == 'forms' and i + 2 < len(path_parts):
            form_id = path_parts[i + 2]
            break

    # Extrair field_ids dos parâmetros
    params = parse_qs(parsed.query)
    field_mapping = {}

    for key, value in params.items():
        if key.startswith('entry.'):
            field_id = key
            field_value = value[0] if value else ''

            # Mapear baseado no conteúdo
            if 'ERRO' in field_value or 'SUCESSO' in field_value:
                field_mapping['tipo'] = field_id
            elif '2024' in field_value or '/' in field_value:
                field_mapping['timestamp'] = field_id
            elif 'processo' in field_value.lower() or len(field_value) > 15:
                field_mapping['processo'] = field_id
            elif 'modelo' in field_value.lower() or 'gpt' in field_value.lower():
                field_mapping['modelo'] = field_id
            elif 'Windows' in field_value or 'Linux' in field_value:
                field_mapping['sistema'] = field_id
            elif 'erro' in field_value.lower() or 'stack' in field_value.lower():
                field_mapping['erro_tecnico'] = field_id
            else:
                field_mapping['descricao'] = field_id

    return form_id, field_mapping

# Uso:
url = "SUA_URL_PREENCHIDA_AQUI"
form_id, fields = extract_form_ids(url)
print(f"FORM_ID = '{form_id}'")
for name, id in fields.items():
    print(f"FIELD_{name.upper()} = '{id}'")
```

### PASSO 3: Implementar Sistema de Feedback

```python
# feedback_system.py
import requests
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import platform
import sys
import traceback

class FeedbackSystem:
    def __init__(self, form_id: str, field_ids: Dict[str, str]):
        """
        Inicializa o sistema de feedback

        Args:
            form_id: ID do Google Form
            field_ids: Dicionário com mapeamento nome_campo -> entry_id
        """
        self.form_id = form_id
        self.field_ids = field_ids
        self.base_url = f"https://docs.google.com/forms/d/e/{form_id}/formResponse"
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

        # Rastreamento de estado
        self._feedback_enviado = False
        self._processo_atual = ""
        self._operacao_sucesso = False

    def _get_system_info(self) -> str:
        """Coleta informações do sistema"""
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'python': sys.version.split()[0],
                'architecture': platform.machine(),
                'processor': platform.processor()
            }
            return json.dumps(info, ensure_ascii=False)
        except:
            return "Sistema desconhecido"

    def _get_stack_trace(self) -> str:
        """Captura o stack trace atual"""
        try:
            return traceback.format_exc()
        except:
            return "Stack trace não disponível"

    def send_feedback(
        self,
        tipo: str,
        processo: str = "",
        modelo: str = "",
        descricao: str = "",
        erro_tecnico: Optional[str] = None,
        incluir_sistema: bool = True
    ) -> bool:
        """
        Envia feedback para o Google Forms

        Args:
            tipo: Tipo de feedback (ERRO, SUCESSO_AUTO, PROBLEMA)
            processo: Identificador do processo/operação
            modelo: Modelo ou configuração usada
            descricao: Descrição detalhada
            erro_tecnico: Informações técnicas de erro (opcional)
            incluir_sistema: Se deve incluir informações do sistema

        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            # Preparar dados
            data = {}

            # Timestamp
            if 'timestamp' in self.field_ids:
                data[self.field_ids['timestamp']] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Tipo de feedback
            if 'tipo' in self.field_ids:
                data[self.field_ids['tipo']] = tipo

            # Processo
            if 'processo' in self.field_ids:
                data[self.field_ids['processo']] = processo or "N/A"

            # Modelo
            if 'modelo' in self.field_ids:
                data[self.field_ids['modelo']] = modelo or "N/A"

            # Descrição
            if 'descricao' in self.field_ids:
                data[self.field_ids['descricao']] = descricao or f"Feedback automático: {tipo}"

            # Sistema
            if incluir_sistema and 'sistema' in self.field_ids:
                data[self.field_ids['sistema']] = self._get_system_info()

            # Erro técnico
            if erro_tecnico and 'erro_tecnico' in self.field_ids:
                data[self.field_ids['erro_tecnico']] = erro_tecnico

            # Enviar para Google Forms
            response = self.session.post(
                self.base_url,
                data=data,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )

            # Verificar sucesso
            if response.status_code in [200, 302]:
                self.logger.info(f"Feedback {tipo} enviado com sucesso")
                self._feedback_enviado = True
                return True
            else:
                self.logger.error(f"Erro ao enviar feedback: HTTP {response.status_code}")
                return False

        except Exception as e:
            self.logger.error(f"Erro ao enviar feedback: {e}")
            return False

    def on_operation_start(self, processo: str):
        """Marca início de uma operação"""
        self._processo_atual = processo
        self._operacao_sucesso = False
        self._feedback_enviado = False
        self.logger.debug(f"Operação iniciada: {processo}")

    def on_operation_success(self):
        """Marca operação como bem-sucedida"""
        self._operacao_sucesso = True
        self.logger.debug(f"Operação concluída com sucesso: {self._processo_atual}")

    def on_operation_error(self, error: Exception, descricao: str = ""):
        """Registra erro na operação"""
        self._operacao_sucesso = False

        # Enviar feedback de erro automaticamente
        erro_tecnico = f"{type(error).__name__}: {str(error)}\n\n{self._get_stack_trace()}"

        self.send_feedback(
            tipo="ERRO",
            processo=self._processo_atual,
            descricao=descricao or f"Erro durante operação: {str(error)}",
            erro_tecnico=erro_tecnico
        )

    def on_application_close(self):
        """Chamado ao fechar a aplicação"""
        if self._operacao_sucesso and not self._feedback_enviado:
            # Enviar feedback positivo automático
            self.send_feedback(
                tipo="SUCESSO_AUTO",
                processo=self._processo_atual,
                descricao="Operação concluída sem erros reportados"
            )
```

### PASSO 4: Integração com Tkinter

```python
# main_app.py
import tkinter as tk
from tkinter import ttk, messagebox
from feedback_system import FeedbackSystem

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configurar feedback system
        self.feedback = FeedbackSystem(
            form_id="SEU_FORM_ID_AQUI",
            field_ids={
                'timestamp': 'entry.123456',
                'tipo': 'entry.234567',
                'processo': 'entry.345678',
                'modelo': 'entry.456789',
                'descricao': 'entry.567890',
                'sistema': 'entry.678901',
                'erro_tecnico': 'entry.789012'
            }
        )

        self.title("Aplicação com Feedback Automático")
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self._build_ui()

    def _build_ui(self):
        # Interface principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campo de entrada
        ttk.Label(main_frame, text="Processo:").grid(row=0, column=0, sticky=tk.W)
        self.processo_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.processo_var, width=50).grid(row=0, column=1, padx=5)

        # Botões
        ttk.Button(main_frame, text="Processar", command=self._processar).grid(row=1, column=0, pady=10)
        ttk.Button(main_frame, text="Reportar Problema", command=self._reportar_problema).grid(row=1, column=1, pady=10)

        # Status
        self.status_var = tk.StringVar(value="Pronto")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=2, column=0, columnspan=2)

    def _processar(self):
        """Processa uma operação"""
        processo = self.processo_var.get()

        if not processo:
            messagebox.showwarning("Aviso", "Digite um número de processo")
            return

        # Marcar início da operação
        self.feedback.on_operation_start(processo)

        try:
            # Simular processamento
            self.status_var.set("Processando...")
            self.update()

            # Aqui vai sua lógica de negócio
            resultado = self._executar_logica_negocio(processo)

            if resultado:
                # Sucesso
                self.feedback.on_operation_success()
                self.status_var.set("Concluído com sucesso!")
                messagebox.showinfo("Sucesso", "Operação concluída!")
            else:
                raise Exception("Falha no processamento")

        except Exception as e:
            # Erro - feedback automático
            self.feedback.on_operation_error(e, f"Erro ao processar: {processo}")
            self.status_var.set(f"Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro durante processamento:\n{str(e)}")

    def _executar_logica_negocio(self, processo):
        """Sua lógica de negócio aqui"""
        # Simular processamento
        import time
        time.sleep(1)

        # Simular 90% de sucesso
        import random
        return random.random() > 0.1

    def _reportar_problema(self):
        """Interface para reportar problema manualmente"""
        # Criar janela de feedback
        feedback_window = tk.Toplevel(self)
        feedback_window.title("Reportar Problema")
        feedback_window.geometry("400x300")
        feedback_window.transient(self)
        feedback_window.grab_set()

        # Campos
        ttk.Label(feedback_window, text="Descreva o problema:").pack(pady=10)

        text_widget = tk.Text(feedback_window, height=10, width=50)
        text_widget.pack(padx=10, pady=5)

        def enviar():
            descricao = text_widget.get("1.0", tk.END).strip()

            if descricao:
                # Enviar feedback
                sucesso = self.feedback.send_feedback(
                    tipo="PROBLEMA",
                    processo=self.processo_var.get(),
                    descricao=descricao
                )

                if sucesso:
                    messagebox.showinfo("Sucesso", "Problema reportado com sucesso!", parent=feedback_window)
                    feedback_window.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao enviar feedback", parent=feedback_window)
            else:
                messagebox.showwarning("Aviso", "Digite uma descrição", parent=feedback_window)

        ttk.Button(feedback_window, text="Enviar", command=enviar).pack(pady=10)
        ttk.Button(feedback_window, text="Cancelar", command=feedback_window.destroy).pack()

    def _on_closing(self):
        """Ao fechar a aplicação"""
        # Enviar feedback automático se necessário
        self.feedback.on_application_close()

        # Fechar
        self.destroy()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
```

### PASSO 5: Configuração para Executável

```python
# config.py
# Configurações do sistema de feedback
FEEDBACK_CONFIG = {
    'enabled': True,  # Habilitar/desabilitar feedback
    'form_id': 'SEU_GOOGLE_FORM_ID',
    'fields': {
        'timestamp': 'entry.123456789',
        'tipo': 'entry.234567890',
        'processo': 'entry.345678901',
        'modelo': 'entry.456789012',
        'descricao': 'entry.567890123',
        'sistema': 'entry.678901234',
        'erro_tecnico': 'entry.789012345'
    },
    'auto_success': True,  # Enviar sucesso automático ao fechar
    'capture_system': True,  # Capturar informações do sistema
    'debug_mode': False  # Modo debug (mais logs)
}
```

### PASSO 6: Script de Teste Completo

```python
# test_feedback.py
import time
from feedback_system import FeedbackSystem

def test_feedback_system():
    """Testa o sistema de feedback"""

    # Configurar
    feedback = FeedbackSystem(
        form_id="SEU_FORM_ID",
        field_ids={
            'timestamp': 'entry.123',
            'tipo': 'entry.456',
            'processo': 'entry.789',
            'descricao': 'entry.012'
        }
    )

    print("Testando sistema de feedback...")

    # Teste 1: Sucesso automático
    print("\n1. Testando feedback de sucesso...")
    resultado = feedback.send_feedback(
        tipo="SUCESSO_AUTO",
        processo="TESTE-001",
        descricao="Teste de feedback automático"
    )
    print(f"   Resultado: {'✓ Enviado' if resultado else '✗ Falhou'}")

    time.sleep(2)

    # Teste 2: Erro
    print("\n2. Testando feedback de erro...")
    try:
        raise ValueError("Erro simulado para teste")
    except Exception as e:
        feedback.on_operation_error(e, "Teste de captura de erro")
    print("   Erro capturado e enviado")

    time.sleep(2)

    # Teste 3: Problema manual
    print("\n3. Testando feedback de problema...")
    resultado = feedback.send_feedback(
        tipo="PROBLEMA",
        processo="TESTE-003",
        descricao="Problema reportado manualmente durante teste"
    )
    print(f"   Resultado: {'✓ Enviado' if resultado else '✗ Falhou'}")

    print("\n✅ Testes concluídos!")
    print("Verifique as respostas no Google Forms")

if __name__ == "__main__":
    test_feedback_system()
```

## 🎯 Benefícios da Implementação

### 1. **Totalmente Gratuito**
- Usa Google Forms como backend
- Sem custos de servidor ou banco de dados
- Sem limites de uso

### 2. **Zero Configuração de Servidor**
- Não precisa de API Keys
- Não precisa de autenticação OAuth
- Funciona com simples requisições POST

### 3. **Coleta Inteligente**
- Feedback automático de sucesso ao fechar
- Captura automática de erros com stack trace
- Informações do sistema incluídas

### 4. **Transparente mas Não Intrusivo**
- Usuário não precisa fazer nada
- Opção de reportar problemas manualmente
- Não afeta performance da aplicação

### 5. **Dados Estruturados**
- Respostas organizadas no Google Sheets
- Fácil análise e estatísticas
- Export para outros formatos

## 📊 Análise dos Dados Coletados

### Acessar Respostas
1. Abra seu Google Form
2. Clique na aba "Respostas"
3. Clique no ícone do Sheets para criar planilha
4. Analise os dados com filtros e gráficos

### Métricas Importantes
- Taxa de sucesso vs erro
- Problemas mais comuns
- Horários de pico de uso
- Sistemas operacionais dos usuários
- Processos que mais geram erros

## 🔒 Considerações de Segurança

1. **Não envie dados sensíveis** (senhas, tokens, etc.)
2. **Anonimize identificadores** se necessário
3. **Use HTTPS** sempre (Google Forms já usa)
4. **Limite informações do sistema** ao necessário
5. **Implemente rate limiting** se necessário

## 🚀 Melhorias Avançadas

### 1. **Versionamento**
Adicione campo de versão para rastrear em qual versão ocorreu o problema

### 2. **Session ID**
Gere um UUID por sessão para agrupar feedbacks relacionados

### 3. **Screenshots**
Para erros visuais, capture e envie screenshot (convertido para base64)

### 4. **Offline Queue**
Armazene feedbacks localmente quando offline e envie quando reconectar

### 5. **Opt-out**
Permita usuários desabilitarem o feedback se desejarem

## 📝 Checklist de Implementação

- [ ] Criar Google Form com campos necessários
- [ ] Extrair IDs dos campos usando script
- [ ] Implementar classe FeedbackSystem
- [ ] Integrar com aplicação principal
- [ ] Adicionar tratamento de erros
- [ ] Implementar feedback automático ao fechar
- [ ] Adicionar botão de reportar problema
- [ ] Testar envio de feedbacks
- [ ] Verificar recebimento no Google Forms
- [ ] Configurar planilha de respostas
- [ ] Documentar para usuários finais
- [ ] Compilar e testar executável

## 💡 Dicas Importantes

1. **Teste em produção**: O comportamento pode variar entre desenvolvimento e executável
2. **Monitore regularmente**: Verifique as respostas semanalmente
3. **Itere baseado no feedback**: Use os dados para melhorar a aplicação
4. **Comunique aos usuários**: Seja transparente sobre a coleta de dados
5. **Mantenha simplicidade**: Não complique demais o sistema

---

**Este sistema de feedback me economizou horas de debug e melhorou drasticamente a qualidade da aplicação. Os dados coletados automaticamente revelaram padrões de uso e problemas que eu nunca teria descoberto sozinho.**