# Changelog

Todas as mudanças notáveis do projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [1.0.0] - 2025-10-01

### 🎉 Release Oficial v1.0.0

Primeira versão estável oficial do Sistema AJG - Assistência Judiciária Gratuita.

### ✨ Novos Recursos

- **Coleta ampliada de movimentos**: Sistema agora coleta descrições de TODOS os movimentos processuais (não apenas decisões/despachos com códigos 3 e 11009)
- **Identificação inteligente de beneficiários**: LLM analisa descrições das decisões para identificar beneficiário específico da justiça gratuita
  - Identifica nomes específicos mencionados nas decisões
  - Analisa termos como "autor", "réu", "requerente", "executado"
  - Processa casos com uma ou múltiplas partes no polo processual
- **Marcador de revisão humana**: Sistema sinaliza com ⚠️ quando há ambiguidade sobre o beneficiário
- **Interface simplificada**: Removida seleção manual de modelo LLM (agora usa Google Gemini 2.5 Flash por padrão)

### 🔧 Melhorias

- **Parser XML robusto**: Coleta todos os movimentos que possuem descrição, independente do `codigoPaiNacional`
- **Prompt LLM aprimorado**: Instruções detalhadas com exemplos práticos de como identificar beneficiários
- **Sistema de revisão integrado**: Orientações claras para revisão humana em casos ambíguos
- **Documentação consolidada**: Toda documentação agora está no README.md principal

### 🧹 Refatoração

- **Limpeza de repositório**: Removidos 13 arquivos obsoletos (testes, debug, documentação redundante)
- **Estrutura simplificada**: Redução de ~30% dos arquivos do repositório
- **Unificação em main_exe.py**: Arquivo `main.py` removido (desenvolvimento e produção agora usam o mesmo arquivo)
- **Pasta docs/ removida**: Conteúdo consolidado no README principal
- **Arquivos de teste removidos**:
  - `extract_form_ids_detailed.py`
  - `test_google_forms_complete.py`
  - `tests/test_config.py`
  - `tests/test_update.py`
- **Scripts auxiliares removidos**: `scripts/cleanup_workflows.py`
- **Pasta test_version/ removida**: Arquivos temporários de testes de versão

### 🐛 Correções

- **Certificados SSL**: Corrigido problema de certificados SSL no executável empacotado com PyInstaller
- **Build automático**: Ajustado workflow do GitHub Actions para build confiável
- **Dependências HTTP**: Otimizada coleta de dependências (requests, urllib3, certifi) no PyInstaller
- **ModuleNotFoundError**: Corrigido problema de importação de módulos no executável

### 📦 Dependências

- Python 3.11+
- Tkinter (interface gráfica)
- Requests + urllib3 + certifi (HTTP stack)
- OpenRouter API (Google Gemini 2.5 Flash)
- PyInstaller 6.0+ (para build do executável)

### 🔄 Alterações Importantes (Breaking Changes)

- **main.py removido**: Agora use `python main_exe.py` para execução em desenvolvimento
- **Pasta docs/ removida**: Consulte README.md para toda documentação
- **Executável renomeado**: De `RelatorioTJMS.exe` para `AJG.exe`
- **Estrutura de pastas**: Arquivos reorganizados para melhor manutenibilidade

### 📋 Detalhes Técnicos

#### Parser XML (main_exe.py:252-317)
- **Antes**: Filtrava apenas movimentos com `codigoPaiNacional` = "3" ou "11009"
- **Depois**: Coleta TODOS os movimentos que tenham descrição, independente do código
- Mantém `codigoPaiNacional` para referência mas não usa como filtro restritivo

#### Prompt LLM (main_exe.py:355-375)
- **Nova seção**: "IMPORTANTE - IDENTIFICAÇÃO DO BENEFICIÁRIO"
- **Lógica implementada**:
  - Se decisão menciona nome específico → associa àquela parte
  - Se termo genérico + UMA parte no polo → associa àquela parte
  - Se termo genérico + MÚLTIPLAS partes → considera todas beneficiadas
  - Se AMBÍGUO/INCERTO → marca com "⚠️ REVISÃO NECESSÁRIA"

#### Exemplos de Saída do Sistema
```
✅ **João da Silva**: Consta no sistema como beneficiário.
   Decisão identificou especificamente esta parte:
   "Defiro a gratuidade ao autor João da Silva" (Despacho, 01/01/2023).

⚠️ **Maria Santos**: Consta no sistema como beneficiária.
   ⚠️ REVISÃO NECESSÁRIA: Há decisão deferindo gratuidade mas não
   especifica qual dos 3 autores foi beneficiado.
```

---

## Versões Anteriores (v1.0.11 - v1.0.28)

Releases de desenvolvimento com builds experimentais. Foram descontinuadas devido a problemas de build e configuração.

### Principais Problemas das Versões Antigas
- Problemas de certificados SSL no executável
- Erros de build do GitHub Actions
- ModuleNotFoundError em ambientes limpos
- Documentação fragmentada e redundante
- Estrutura de arquivos confusa

Todas essas questões foram resolvidas na versão 1.0.0.

---

## Como Usar Este Changelog

- **Usuários**: Consulte a seção da versão atual para saber o que mudou
- **Desenvolvedores**: Use como referência para mudanças técnicas e breaking changes
- **Releases Futuras**: Seguir o mesmo formato para documentar mudanças

---

**Convenções de Versionamento**: Semantic Versioning (MAJOR.MINOR.PATCH)
- MAJOR: Mudanças incompatíveis na API/interface
- MINOR: Nova funcionalidade mantendo compatibilidade
- PATCH: Correções de bugs mantendo compatibilidade
