# 🔑 Configuração Fácil de Chave API

## 🎯 **NOVA FUNCIONALIDADE: Setup Automático**

Agora o sistema pede a chave OpenRouter automaticamente na primeira execução e salva para uso futuro!

## 🚀 **Como funciona:**

### **1. Primeira execução no outro computador**
1. Execute `RelatorioTJMS.exe`
2. Uma janela aparecerá pedindo a chave OpenRouter
3. Siga as instruções para obter sua chave
4. Cole a chave e clique "Salvar"
5. ✅ **Pronto!** A chave fica salva automaticamente

### **2. Execuções seguintes**
- O programa carrega a chave salva automaticamente
- ✅ **Não precisa configurar novamente!**

### **3. Se a chave mudar**
- Clique no botão **"⚙️ Configurar Chave"** na interface
- Insira a nova chave
- ✅ **Atualizada automaticamente!**

## 🔒 **Segurança:**

- **Chave criptografada:** Salva com codificação Base64
- **Arquivo local:** `.relatorio_config` na pasta do programa
- **Não sincroniza:** Cada computador tem sua própria configuração
- **Validação automática:** Testa se a chave funciona antes de salvar

## 📱 **Interface amigável:**

### **Dialog de configuração inicial:**
```
🔑 Configuração da Chave OpenRouter
=================================

Como obter sua chave:
1. Acesse: https://openrouter.ai/keys
2. Faça login ou crie uma conta
3. Clique em "Create Key"
4. Copie a chave (sk-or-v1-...)
5. Cole abaixo:

Chave OpenRouter: [••••••••••••••••••••]
☐ Mostrar chave

[Cancelar] [Salvar]
```

### **Botões na interface principal:**
- **"⚙️ Configurar Chave"** - Reconfigurar chave API
- **"🔄 Verificar Atualizações"** - Auto-update

## 🎛️ **Ordem de prioridade das chaves:**

1. **Variável de ambiente** `OPENROUTER_API_KEY`
2. **Arquivo .env** (desenvolvimento)
3. **config_local.py** (desenvolvimento)
4. **🆕 Chave salva pelo sistema** ← **NOVA FUNCIONALIDADE**
5. **Placeholder** (pede configuração)

## 🔄 **Fluxo completo:**

```
[Usuário executa .exe]
         ↓
[Sistema verifica chave]
         ↓
[Chave existe?] → SIM → [Programa funciona]
         ↓
        NÃO
         ↓
[Mostra dialog de configuração]
         ↓
[Usuário insere chave]
         ↓
[Sistema valida com API]
         ↓
[Chave válida?] → NÃO → [Mostra erro, pede novamente]
         ↓
        SIM
         ↓
[Salva chave localmente]
         ↓
[Programa funciona normalmente]
```

## 🛠️ **Para desenvolvedores:**

### **Compilar com nova funcionalidade:**
```bash
python build_exe.py
```

### **Testar key manager:**
```python
from key_manager import get_api_key

# Primeira configuração
key = get_api_key()

# Forçar nova configuração
key = get_api_key(force_new=True)
```

### **Arquivos criados:**
- `key_manager.py` - Gerenciador de chaves
- `.relatorio_config` - Arquivo de configuração (criado automaticamente)

## 📋 **Vantagens da nova abordagem:**

✅ **Zero configuração manual** no outro computador
✅ **Interface gráfica intuitiva** para configuração
✅ **Validação automática** da chave com a API
✅ **Armazenamento seguro** local
✅ **Fácil reconfiguração** se chave mudar
✅ **Compatível** com métodos anteriores
✅ **Feedback claro** para o usuário

## 🎉 **Resultado:**

**Distribuição simplificada:**
1. Gere o executável: `python build_exe.py`
2. Copie `RelatorioTJMS.exe` para outro computador
3. Execute uma vez → configura automaticamente
4. ✅ **Funciona para sempre!**

---

**Experiência do usuário final completamente otimizada!** 🚀