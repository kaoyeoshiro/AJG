# 🔒 Como Baixar e Usar o AJG com Segurança

## 🚨 IMPORTANTE: O executável é seguro!

O Windows Defender pode bloquear o arquivo **AJG.exe** porque:
- É um executável Python compilado (comum serem detectados como falso positivo)
- Não possui assinatura digital cara (certificados custam centenas de dólares)
- Faz requisições de rede (comportamento comum em malware, mas necessário aqui)

**🛡️ Garantimos que é seguro porque:**
- ✅ Código fonte 100% aberto no GitHub
- ✅ Build automatizado e público no GitHub Actions
- ✅ Checksums para verificação de integridade
- ✅ Histórico completo de todas as mudanças

## 📥 Como Baixar Corretamente

### 1. **Sempre baixe do GitHub Releases**
🔗 **Link oficial:** https://github.com/SEU_USUARIO/SEU_REPOSITORIO/releases

⚠️ **NUNCA baixe de outros sites** - apenas do GitHub oficial!

### 2. **Baixe a versão mais recente**
- Clique na versão mais recente (ex: v1.2.3)
- Baixe o arquivo **AJG.exe**
- Opcionalmente baixe **SECURITY.md** e **SHA256SUMS**

## 🛡️ Como Contornar o Windows Defender

### Método 1: Permitir uma vez
1. O Windows vai mostrar uma tela vermelha "Windows protegeu seu PC"
2. Clique em **"Mais informações"**
3. Clique em **"Executar assim mesmo"**

### Método 2: Exceção permanente (recomendado)
1. Abra **Windows Security** (Windows Defender)
2. Vá em **"Proteção contra vírus e ameaças"**
3. Clique em **"Gerenciar configurações"**
4. Role até **"Exclusões"** e clique **"Adicionar ou remover exclusões"**
5. Clique **"Adicionar uma exclusão"** → **"Arquivo"**
6. Selecione o arquivo **AJG.exe**

### Método 3: Exceção por pasta
1. Siga os passos do Método 2 até o item 5
2. Escolha **"Pasta"** em vez de "Arquivo"
3. Selecione a pasta onde está o AJG.exe

## 🔍 Verificar Integridade (Opcional)

### Usando PowerShell:
```powershell
# Navegar até a pasta do download
cd "C:\Users\SEU_USUARIO\Downloads"

# Verificar SHA256
Get-FileHash AJG.exe -Algorithm SHA256

# Verificar se está assinado (se disponível)
Get-AuthenticodeSignature AJG.exe
```

### Usando Command Prompt:
```cmd
cd C:\Users\SEU_USUARIO\Downloads
certutil -hashfile AJG.exe SHA256
```

Compare o resultado com o hash no arquivo **SHA256SUMS** do release.

## ⚙️ Configuração Inicial

### 1. **Obter Chave OpenRouter**
1. Acesse: https://openrouter.ai/keys
2. Faça login/cadastro
3. Crie uma nova chave API
4. **Guarde a chave** (ela será mostrada apenas uma vez)

### 2. **Configurar no Programa**
1. Execute o **AJG.exe**
2. Clique no botão **"⚙️ Configurar Chave"**
3. Cole sua chave OpenRouter
4. Clique em **"Salvar"**

### 3. **Alternativa: Configurar Manualmente**
Se o botão não funcionar:
1. Edite o arquivo **config.py** (se disponível)
2. Linha 57: substitua `"SUA_CHAVE_AQUI"` pela sua chave
3. Salve o arquivo

## 🚨 Sinais de Arquivo Comprometido

🚩 **CUIDADO se:**
- Baixou de site que não seja o GitHub oficial
- O arquivo tem tamanho muito diferente do esperado
- O hash SHA256 não confere com o oficial
- Pede permissões estranhas (rede, administrador, etc.)

## 📞 Suporte e Ajuda

### Se ainda tiver problemas:
1. **Abra uma issue:** https://github.com/SEU_USUARIO/SEU_REPOSITORIO/issues
2. **Inclua informações:**
   - Versão do Windows
   - Versão do AJG baixada
   - Mensagem de erro completa
   - Passos que levaram ao problema

### Contatos:
- 🐛 **Issues:** GitHub Issues (preferencial)
- 📧 **Email:** [se disponível]
- 💬 **Chat:** [se disponível]

## 🔄 Atualizações

- O programa verifica atualizações automaticamente
- Sempre use a versão mais recente para segurança
- Releases são publicados no GitHub com changelog completo

---

## ✅ Checklist de Segurança

Antes de executar, confirme:

- [ ] Baixado do GitHub oficial
- [ ] Versão mais recente
- [ ] Hash SHA256 confere (opcional)
- [ ] Windows Defender configurado (exceção)
- [ ] Chave OpenRouter configurada

**🎯 Com estes passos, você terá um sistema 100% funcional e seguro!**