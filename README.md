# Sistema de Relatórios TJ-MS

Sistema automatizado para consulta de processos e geração de relatórios via LLM integrado ao Tribunal de Justiça de Mato Grosso do Sul.

## Visão Geral

O Sistema de Relatórios TJ-MS é uma aplicação desktop que automatiza o processo de consulta de dados processuais no TJ-MS e gera relatórios estruturados utilizando inteligência artificial. O sistema oferece uma interface gráfica intuitiva, sistema de feedback integrado, atualizações automáticas e múltiplos formatos de exportação.

### Principais Funcionalidades

- **Consulta TJ-MS**: Integração via SOAP com validação CNJ automática
- **Geração de Relatórios**: Utiliza LLM (OpenRouter) para análise e estruturação de dados
- **Interface Gráfica**: Aplicação desktop intuitiva com logs integrados em tempo real
- **Múltiplos Formatos**: Exportação em DOCX, PDF e TXT
- **Sistema de Feedback**: Coleta automática de feedback para melhoria contínua
- **Auto-Atualização**: Sistema integrado de atualizações via GitHub
- **Templates Personalizáveis**: Suporte a templates DOCX customizados

## Quick Start

### Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/kaoyeoshiro/AJG.git
   cd AJG
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as credenciais**:
   ```bash
   copy .env.example .env
   # Edite o arquivo .env com suas credenciais
   ```

4. **Execute o sistema**:
   ```bash
   python main_exe.py
   ```

### Usando o Executável

Para uso em produção, baixe o executável mais recente em [Releases](https://github.com/kaoyeoshiro/AJG/releases):

1. Baixe `AJG.exe`
2. Execute o arquivo
3. Na primeira execução, configure sua chave OpenRouter quando solicitado
4. O sistema estará pronto para uso

## Configuração

### Configuração Automática de Chave API (Recomendado)

O sistema possui um gerenciador de chaves que facilita a configuração:

**Primeira Execução:**
1. Execute `AJG.exe`
2. Uma janela solicitará sua chave OpenRouter
3. Acesse [openrouter.ai/keys](https://openrouter.ai/keys) para obter sua chave
4. Cole a chave e clique "Salvar"
5. A chave fica salva automaticamente para uso futuro

**Reconfiguração:**
- Clique no botão "⚙️ Configurar Chave" na interface principal
- Insira a nova chave quando necessário

### Configuração Manual (.env)

Crie um arquivo `.env` baseado no `.env.example`:

```env
# Credenciais TJ-MS
TJ_WSDL_URL=https://seu-tjms-wsdl-url
TJ_WS_USER=seu_usuario
TJ_WS_PASS=sua_senha

# Chave OpenRouter
OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui

# Sistema de Feedback (opcional)
GOOGLE_FORM_URL=https://docs.google.com/forms/d/SEU_ID/formResponse
GOOGLE_FORM_FIELD_TIPO=entry.1234567890
GOOGLE_FORM_FIELD_DESCRICAO=entry.0987654321
GOOGLE_FORM_FIELD_PROCESSO=entry.1122334455
GOOGLE_FORM_FIELD_MODELO=entry.5566778899
GOOGLE_FORM_FIELD_TIMESTAMP=entry.9988776655
GOOGLE_FORM_FIELD_VERSAO=entry.1357924680
```

### Ordem de Prioridade para Configurações

O sistema busca as configurações na seguinte ordem:

1. **Variável de ambiente** `OPENROUTER_API_KEY`
2. **Arquivo .env** (desenvolvimento)
3. **config_local.py** (desenvolvimento)
4. **Chave salva pelo sistema** (gerenciador automático)
5. **Placeholder** (solicita configuração)

## Sistema de Feedback

O sistema coleta feedback automaticamente para melhorar a qualidade dos relatórios:

### Como Funciona

- **Feedback Negativo**: Usuário clica "⚠️ Reportar Erro" quando há problemas no relatório
- **Feedback Positivo Automático**: Enviado quando:
  - Usuário gera novo relatório sem reportar erro no anterior
  - Usuário fecha o sistema sem reportar erro no relatório atual
- **Botões Inteligentes**: Controles só ficam ativos após gerar relatório com sucesso

### Configuração do Google Forms

#### 1. Criar Formulário

1. Acesse [forms.google.com](https://forms.google.com)
2. Crie um formulário: "Feedback - Sistema Relatórios TJ-MS"
3. Adicione os campos na ordem exata:

   - **Tipo de Feedback** (múltipla escolha): ERRO, SUCESSO_AUTO
   - **Descrição do Problema** (resposta longa)
   - **Número do Processo CNJ** (resposta curta)
   - **Modelo LLM Utilizado** (resposta curta)
   - **Data e Hora** (resposta curta)
   - **Versão do Sistema** (resposta curta)

#### 2. Obter URLs e IDs

1. **URL de Envio**: Substitua `/viewform` por `/formResponse` na URL do formulário
2. **IDs dos Campos**: Use F12 no navegador e execute:
   ```javascript
   document.querySelectorAll('[name^="entry."]').forEach(function(field, index) {
       console.log('Campo ' + (index + 1) + ': ' + field.name);
   });
   ```

#### 3. Configurar Planilha

1. Na aba "Respostas" do Forms, conecte uma planilha Google Sheets
2. A planilha receberá automaticamente todos os feedbacks

## Formatos de Saída e Templates

### Formatos Suportados

1. **DOCX** (recomendado): Formatação completa com templates personalizáveis
2. **PDF**: Conversão automática via LibreOffice ou docx2pdf
3. **TXT**: Backup em texto simples

### Templates DOCX

Crie templates personalizados:

1. Crie o diretório `templates/`
2. Adicione seu template como `templates/template.docx`
3. Use marcadores no template que serão substituídos pelo conteúdo do relatório
4. O sistema aplicará automaticamente o template nos relatórios DOCX

## Building e Deployment

### Build Local

**Pré-requisitos:**
- Python 3.8+
- Dependências instaladas (`pip install -r requirements.txt`)

**Processo:**

1. **Configure credenciais no código**:
   ```bash
   # Edite config.py com suas credenciais reais
   python build_exe.py
   ```

2. **Build automático com chave** (recomendado):
   ```bash
   python build_with_key.py
   ```

3. **Teste o executável**:
   ```bash
   dist/AJG.exe
   ```

### Build Automático (GitHub Actions)

O sistema possui build automático configurado:

**Funcionalidades:**
- Build automático a cada push no branch `master`
- Geração de releases automáticas
- Versionamento incremental
- Executável disponível em GitHub Releases

**Configuração Segura:**
1. Configure `OPENROUTER_API_KEY` como Secret no GitHub:
   - Acesse: Settings → Secrets and variables → Actions
   - Adicione: `OPENROUTER_API_KEY` com sua chave

**Workflow:**
```bash
# 1. Fazer alterações no código
git add .
git commit -m "Descrição das alterações"
git push origin master

# 2. GitHub Actions automaticamente:
#    - Executa build do executável
#    - Cria nova release
#    - Disponibiliza download
```

## Sistema de Auto-Atualização

### Como Funciona

O executável possui sistema integrado de atualizações:

- **Verificação Automática**: Ao iniciar, verifica novas versões silenciosamente
- **Atualização Manual**: Botão "🔄 Verificar Atualizações" na interface
- **Download e Aplicação**: Atualização automática com reinicialização do programa

### Versionamento

- Versões automáticas baseadas no build: `v1.0.1`, `v1.0.2`, etc.
- Controle via GitHub Actions
- Arquivo `VERSION` contém versão atual

### Para Usuários

1. **Atualização Manual**:
   - Clique "🔄 Verificar Atualizações"
   - Confirme se houver nova versão
   - Programa atualiza e reinicia automaticamente

2. **Atualização Automática**:
   - Sistema verifica atualizações ao iniciar
   - Notificação discreta se nova versão disponível

## Segurança e Boas Práticas

### Proteção de Credenciais

- **Sem hardcoding**: Chaves nunca ficam no código fonte
- **Variáveis de ambiente**: Configuração segura via `.env`
- **GitHub Secrets**: Build automático sem exposição de credenciais
- **Criptografia local**: Chaves salvas com codificação Base64

### Arquivo .gitignore

O projeto já inclui `.gitignore` configurado para proteger:
```
.env
config_local.py
.relatorio_config
__pycache__/
build/
dist/
*.pyc
```

### Validação de Entrada

- **CNJ**: Validação automática de números de processo
- **API**: Verificação de chaves antes de salvar
- **Dados**: Sanitização de entradas do usuário

## Troubleshooting

### Problemas Comuns

**Erro: "Configurações não preenchidas"**
- Verifique se o arquivo `.env` existe e está preenchido
- Confirme se não há valores placeholder como `"SEU_*_AQUI"`

**Erro: "Falha na consulta TJ-MS"**
- Verifique credenciais do webservice
- Teste conectividade de rede
- Valide formato do número CNJ

**Executável bloqueado por antivírus**
- Normal para executáveis PyInstaller
- Adicione exceção no antivírus
- Baixe versão mais recente do GitHub

**Auto-update não funciona**
- Verifique conexão com internet
- Confirme se há releases no GitHub
- Teste manualmente no navegador: `https://api.github.com/repos/kaoyeoshiro/AJG/releases/latest`

### Logs e Debug

- **Interface**: Painel direito mostra logs em tempo real
- **Modo DEBUG**: Ative para informações detalhadas
- **Arquivo de log**: Logs salvos automaticamente
- **Feedback**: Sistema de reportar erros integrado

### Sistema de Feedback com Problemas

**Erro: "URL do Google Forms não configurada"**
- Verifique `GOOGLE_FORM_URL` no `.env`
- Confirme que URL termina com `/formResponse`

**Formulário não recebe dados**
- Teste preenchimento manual no navegador
- Confirme IDs dos campos com F12
- Verifique se formulário aceita respostas

## Desenvolvimento

### Estrutura do Projeto

```
projeto/
├── .github/workflows/          # GitHub Actions
├── scripts/                   # Scripts auxiliares
│   ├── build.py              # Script de build
│   ├── key_manager.py        # Gerenciador de chaves
│   └── updater.py            # Sistema de atualização
├── templates/                 # Templates DOCX/RTF
├── tests/                     # Testes (para desenvolvimento futuro)
├── main_exe.py                # Aplicação principal
├── config.py                  # Configurações
├── build_exe.py               # Script de build local
├── requirements.txt           # Dependências Python
├── .env.example              # Exemplo de configuração
├── AJG.spec                  # Configuração PyInstaller
├── VERSION                    # Versão atual
└── dist/                     # Executável compilado (ignorado)
```

### Contribuindo

1. Fork o repositório
2. Crie branch para sua feature: `git checkout -b feature/nova-funcionalidade`
3. Commit suas alterações: `git commit -m "Adiciona nova funcionalidade"`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra Pull Request

### Testes

Execute testes locais:
```bash
# Teste manual completo
python main_exe.py

# Teste de build
python build_exe.py

# Teste do executável
dist/AJG.exe
```

## Monitoramento

### Métricas Disponíveis

- **Feedback**: Planilha Google Sheets com dados de uso
- **Versões**: GitHub Releases com estatísticas de download
- **Logs**: Sistema de logging integrado para debug

### API GitHub

Consulte informações via API:
```bash
# Versão mais recente
curl https://api.github.com/repos/kaoyeoshiro/AJG/releases/latest

# Todas as releases
curl https://api.github.com/repos/kaoyeoshiro/AJG/releases
```

## Suporte

### Recursos de Ajuda

- **Logs Integrados**: Painel direito da interface com informações detalhadas
- **Validação Automática**: Sistema detecta e reporta problemas automaticamente
- **Fallbacks**: Funcionalidades críticas têm alternativas em caso de falha
- **Feedback Integrado**: Reporte problemas diretamente pela interface

### Canais de Suporte

- **Issues GitHub**: [https://github.com/kaoyeoshiro/AJG/issues](https://github.com/kaoyeoshiro/AJG/issues)
- **Logs do Sistema**: Informações detalhadas no painel da aplicação
- **GitHub Actions**: Logs de build em caso de problemas de atualização

### Documentação Adicional

Toda a documentação foi consolidada neste README principal para facilitar o acesso e manutenção.

---

**Sistema desenvolvido para otimizar o trabalho da Assistência Judiciária** ⚖️

**Versão**: Verifique o arquivo `VERSION` ou a interface do programa
**Licença**: Consulte o arquivo LICENSE do repositório
**Última Atualização**: Consulte os commits mais recentes no GitHub