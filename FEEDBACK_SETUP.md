# 📝 Configuração do Sistema de Feedback

Este documento explica como configurar o sistema de feedback para capturar erros reportados pelos usuários e feedbacks automáticos positivos.

## 🎯 Como Funciona

- **Feedback Negativo**: Usuário clica em "⚠️ Reportar Erro no Conteúdo do Relatório" quando há problemas no relatório
- **Feedback Positivo Automático**: Enviado automaticamente quando:
  - Usuário gera um novo relatório (sem ter reportado erro no anterior)
  - Usuário fecha o sistema (sem ter reportado erro no relatório atual)
- **Apenas para Sucessos**: Sistema só permite feedback em relatórios gerados com sucesso (não para erros de sistema)
- **Botões Inteligentes**: JSON, Salvar e Reportar Erro só ficam ativos após relatório ser gerado

## 📋 Passo 1: Criar Google Forms

### 1.1. Acessar Google Forms
1. Acesse [forms.google.com](https://forms.google.com)
2. Clique em "➕ Criar formulário em branco"
3. Nomeie o formulário: **"Feedback - Sistema Relatórios TJ-MS"**

### 1.2. Configurar Campos do Formulário

Adicione os seguintes campos **EXATAMENTE** nesta ordem:

#### Campo 1: Tipo de Feedback
- **Tipo**: Múltipla escolha
- **Pergunta**: "Tipo de Feedback"
- **Opções**: 
  - ERRO
  - SUCESSO_AUTO
- **Obrigatório**: ✅ Sim

#### Campo 2: Descrição
- **Tipo**: Resposta longa
- **Pergunta**: "Descrição do Problema"
- **Obrigatório**: ✅ Sim

#### Campo 3: Número do Processo
- **Tipo**: Resposta curta
- **Pergunta**: "Número do Processo CNJ"
- **Obrigatório**: ✅ Sim

#### Campo 4: Modelo LLM
- **Tipo**: Resposta curta
- **Pergunta**: "Modelo LLM Utilizado"
- **Obrigatório**: ✅ Sim

#### Campo 5: Data/Hora
- **Tipo**: Resposta curta
- **Pergunta**: "Data e Hora"
- **Obrigatório**: ✅ Sim

#### Campo 6: Versão do Sistema
- **Tipo**: Resposta curta
- **Pergunta**: "Versão do Sistema"
- **Obrigatório**: ❌ Não

### 1.3. Configurar Respostas
1. Clique na aba **"Respostas"**
2. Clique no ícone do **Google Sheets** (planilha)
3. Escolha **"Criar nova planilha"**
4. Nome da planilha: **"Feedback Relatórios TJ-MS"**

## 📋 Passo 2: Obter URLs e IDs

### 2.1. URL de Envio
1. No Google Forms, clique em **"Enviar"** (canto superior direito)
2. Clique no ícone de **"Link"** 
3. **COPIE** a URL que aparece
4. **MODIFIQUE** a URL: substitua `/viewform` por `/formResponse`

**Exemplo:**
- URL original: `https://docs.google.com/forms/d/1ABC123XYZ/viewform`
- URL modificada: `https://docs.google.com/forms/d/1ABC123XYZ/formResponse`

### 2.2. IDs dos Campos
1. Abra a URL original do formulário em uma nova aba
2. Pressione **F12** (Ferramentas do Desenvolvedor)
3. Na aba **"Console"**, cole e execute este código:

```javascript
document.querySelectorAll('[name^="entry."]').forEach(function(field, index) {
    console.log('Campo ' + (index + 1) + ': ' + field.name);
});
```

**MÉTODO ALTERNATIVO** (copie linha por linha se necessário):
```javascript
var campos = document.querySelectorAll('[name^="entry."]');
for (var i = 0; i < campos.length; i++) {
    console.log('Campo ' + (i + 1) + ': ' + campos[i].name);
}
```

**MÉTODO MANUAL** (se os códigos não funcionarem):
1. Pressione **F12** → aba **"Elements"**
2. Pressione **Ctrl+F** e procure por: `entry.`
3. Anote manualmente cada `name="entry.XXXXXXXXXX"` que encontrar

4. **ANOTE** os IDs que aparecerem no console. Deve ser algo como:
   ```
   Tipo de Feedback: entry.1234567890
   Descrição do Problema: entry.0987654321
   Número do Processo CNJ: entry.1122334455
   Modelo LLM Utilizado: entry.5566778899
   Data e Hora: entry.9988776655
   Versão do Sistema: entry.1357924680
   ```

## 📋 Passo 3: Configurar Arquivo .env

Adicione as seguintes linhas ao seu arquivo `.env`:

```env
# ==========================================
# CONFIGURAÇÃO DO SISTEMA DE FEEDBACK
# ==========================================

# URL do Google Forms (substitua pela sua URL com /formResponse)
GOOGLE_FORM_URL=https://docs.google.com/forms/d/SUA_ID_DO_FORMULARIO/formResponse

# IDs dos campos (substitua pelos IDs reais obtidos no Passo 2.2)
GOOGLE_FORM_FIELD_TIPO=entry.1234567890
GOOGLE_FORM_FIELD_DESCRICAO=entry.0987654321
GOOGLE_FORM_FIELD_PROCESSO=entry.1122334455
GOOGLE_FORM_FIELD_MODELO=entry.5566778899
GOOGLE_FORM_FIELD_TIMESTAMP=entry.9988776655
GOOGLE_FORM_FIELD_VERSAO=entry.1357924680
```

## 📋 Passo 4: Testar o Sistema

### 4.1. Teste Manual
1. Execute o sistema: `python main.py`
2. Gere um relatório com sucesso
3. Clique em **"⚠️ Reportar Erro"**
4. Preencha o formulário e envie
5. Verifique se aparece na planilha do Google Sheets

### 4.2. Teste Automático
1. Gere um relatório com sucesso
2. **NÃO** clique em "Reportar Erro"
3. Aguarde 30 segundos
4. Verifique se aparece um feedback automático "SUCESSO_AUTO" na planilha

## 📊 Estrutura da Planilha Resultante

A planilha no Google Sheets terá as seguintes colunas:

| Coluna | Conteúdo | Exemplo |
|--------|----------|---------|
| A | Carimbo de data/hora | 11/09/2024 14:30:25 |
| B | Tipo de Feedback | ERRO ou SUCESSO_AUTO |
| C | Descrição do Problema | "O nome da parte estava incorreto..." |
| D | Número do Processo CNJ | 1234567-89.2020.1.23.4567 |
| E | Modelo LLM Utilizado | openai/gpt-4o-mini |
| F | Data e Hora | 2024-09-11 14:30:25 |
| G | Versão do Sistema | v1.0 |

## 🔧 Troubleshooting

### Erro: "URL do Google Forms não configurada"
- Verifique se `GOOGLE_FORM_URL` está no `.env`
- Certifique-se de que a URL termina com `/formResponse`

### Erro: "Falha ao enviar feedback"
- Verifique se os IDs dos campos estão corretos
- Teste o formulário manualmente no navegador
- Verifique se o formulário está "público" (aceita respostas)

### Formulário não recebe dados
1. Abra o formulário original no navegador
2. Preencha manualmente para testar
3. Verifique se os campos são obrigatórios
4. Confirme os IDs dos campos novamente

## 🎯 Configurações Opcionais

### Personalizar Tempo de Feedback Automático
No arquivo `main.py`, linha que contém:
```python
self.after(30000, self._send_automatic_positive_feedback)
```
Altere `30000` para o tempo desejado em milissegundos (30000 = 30 segundos).

### Desabilitar Feedback Automático
Comente ou remova a linha mencionada acima se não quiser feedback automático.

## ✅ Verificação Final

Após configurar tudo:

1. ✅ Google Forms criado com 6 campos
2. ✅ Planilha conectada ao Forms  
3. ✅ URL `/formResponse` configurada no `.env`
4. ✅ IDs dos campos configurados no `.env`
5. ✅ Teste manual funcionando
6. ✅ Teste automático funcionando

**Sistema de feedback configurado com sucesso!** 🎉
