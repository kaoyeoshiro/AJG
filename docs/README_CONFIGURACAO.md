# 🚀 Sistema de Relatórios TJ-MS

Sistema automatizado para consulta de processos e geração de relatórios via LLM.

## 📁 Arquivos de Configuração

### 🔧 Configuração Básica
- **`env_example.txt`** - Exemplo de configuração do arquivo `.env`
- Copie para `.env` e preencha com suas credenciais

### 📝 Sistema de Feedback  
- **`FEEDBACK_SETUP.md`** - Instruções **COMPLETAS** para configurar feedback via Google Forms
- **LEIA ESTE ARQUIVO** para implementar o sistema de feedback

## ⚡ Instalação Rápida

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   # OU execute: install_optional.bat
   ```

2. **Configurar credenciais:**
   ```bash
   copy env_example.txt .env
   # Edite o .env com suas credenciais
   ```

3. **Configurar feedback (opcional mas recomendado):**
   - Siga o guia completo em `FEEDBACK_SETUP.md`

4. **Executar:**
   ```bash
   python main.py
   ```

## 🎯 Funcionalidades

### ✅ Principais
- **Consulta TJ-MS** via SOAP com validação CNJ
- **Geração de relatórios** via LLM (OpenRouter)
- **Export em DOCX/PDF** com templates personalizáveis
- **Interface gráfica** intuitiva com logs integrados

### ✅ Sistema de Feedback
- **Reportar erros** quando relatório estiver incorreto
- **Feedback automático positivo** quando:
  - Gerar novo relatório (sem ter reportado erro no anterior)
  - Fechar sistema (sem ter reportado erro no atual)
- **Integração com Google Forms** e planilhas
- **Apenas para sucessos** (não para erros do sistema)
- **Botões inteligentes** (só ativos após gerar relatório)

## 📊 Formatos de Saída

1. **DOCX** (recomendado) - Formatação completa, templates
2. **PDF** - Via conversão DOCX (LibreOffice ou docx2pdf)  
3. **TXT** - Backup simples

## 🔍 Templates

- **DOCX**: Crie `templates/template.docx` no Word/LibreOffice
- **RTF**: Descontinuado, use DOCX

## 🆘 Suporte

- **Logs detalhados** no painel direito da interface
- **Modo DEBUG** para troubleshooting
- **Validação automática** de CNJ
- **Fallbacks** para todas as funcionalidades críticas

---

**Sistema desenvolvido para otimizar o trabalho da Assistência Judiciária** ⚖️
