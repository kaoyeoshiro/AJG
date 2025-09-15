# 🔐 Configuração Segura - API Keys e Secrets

## ⚠️ PROBLEMA RESOLVIDO

A chave da OpenRouter foi **removida do código** e agora usa variáveis de ambiente seguras.

## 🚀 Configuração GitHub Secrets

### Passo 1: Adicionar Secret no GitHub
1. Vá para: https://github.com/kaoyeoshiro/AJG/settings/secrets/actions
2. Clique em **"New repository secret"**
3. Name: `OPENROUTER_API_KEY`
4. Value: `sua-nova-chave-openrouter-aqui`
5. Clique **"Add secret"**

### Passo 2: Obter Nova Chave OpenRouter
1. Acesse: https://openrouter.ai/keys
2. Clique **"Create Key"**
3. Copie a nova chave (sk-or-v1-...)
4. Cole no GitHub Secret (Passo 1)

## 🔧 Configuração Local (Desenvolvimento)

### Opção 1: Arquivo .env (RECOMENDADO)
```bash
# Crie arquivo .env (já está no .gitignore)
OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui
```

### Opção 2: Variável de Ambiente
```bash
# Windows
set OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui

# Linux/Mac
export OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui
```

### Opção 3: config_local.py
```python
# Crie config_local.py (já está no .gitignore)
OPENROUTER_API_KEY = "sk-or-v1-sua-chave-aqui"
```

## 🛠️ Para Compilar o Executável com Chave

### Opção 1: Build Automático com Chave (RECOMENDADO)
```bash
python build_with_key.py
```
Este script:
- ✅ Detecta sua chave automaticamente
- ✅ Compila o executável com chave integrada
- ✅ Restaura config original após build

### Opção 2: Configuração Manual
1. Edite `config.py` linha 37:
   ```python
   OPENROUTER_API_KEY = "sk-or-v1-sua-chave-aqui"
   ```
2. Execute: `python build_exe.py`
3. **IMPORTANTE:** Desfaça a mudança antes de commit!

## ✅ Verificar Configuração

```python
import config
print("✅ OK" if config.OPENROUTER_API_KEY else "❌ Chave não configurada")
```

## 🔄 Build Seguro

O GitHub Actions agora:
- ✅ Usa variáveis de ambiente seguras
- ✅ Não expõe chaves nos logs
- ✅ Gera executável com chave injetada

## 📋 Checklist de Segurança

- [x] ✅ Chave removida do código fonte
- [x] ✅ GitHub Secret configurado
- [x] ✅ .gitignore atualizado
- [x] ✅ Build process seguro
- [ ] ⏳ **VOCÊ PRECISA:** Configurar nova chave no GitHub Secrets

---

## 🚨 **AÇÃO NECESSÁRIA**

Antes do próximo build, você deve:

1. **Obter nova chave OpenRouter** (a antiga foi revogada)
2. **Configurar GitHub Secret** com nome `OPENROUTER_API_KEY`
3. **Fazer push** - o build automático funcionará

**GitHub Secrets:** https://github.com/kaoyeoshiro/AJG/settings/secrets/actions