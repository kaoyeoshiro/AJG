# 🚀 Sistema de Auto-Atualização - Relatório TJ-MS

## 📋 Visão Geral

O Sistema de Relatórios TJ-MS agora conta com **atualização automática** que funciona de forma integrada com o GitHub. Sempre que você fizer um push para o repositório, uma nova versão do executável será gerada automaticamente e disponibilizada para download.

## 🔄 Como Funciona

### 1. **Build Automático no GitHub Actions**
- Toda alteração no branch `master` dispara um build automático
- O executável é compilado no Windows usando PyInstaller
- Uma nova release é criada automaticamente no GitHub

### 2. **Auto-Updater Integrado**
- O executável verifica automaticamente se há novas versões disponíveis
- Botão "🔄 Verificar Atualizações" na interface
- Download e aplicação automática da atualização

### 3. **Versionamento Automático**
- Versões são numeradas automaticamente: `v1.0.1`, `v1.0.2`, etc.
- Baseado no número do build do GitHub Actions

## 🛠️ Configuração Inicial

### Passo 1: Ativar GitHub Actions
O arquivo `.github/workflows/build-release.yml` já está configurado e funcionará automaticamente quando você fizer push das mudanças.

### Passo 2: Primeira Release
Para criar a primeira versão:

```bash
# 1. Commit e push das alterações
git add .
git commit -m "Adiciona sistema de auto-atualização"
git push origin master

# 2. Criar primeira tag (opcional)
git tag v1.0.0
git push origin v1.0.0
```

### Passo 3: Configurar Permissões
Certifique-se de que o repositório GitHub tem as permissões necessárias:
- Settings → Actions → General
- Workflow permissions: "Read and write permissions" ✅

## 📥 Como Usar (Para Usuários Finais)

### Atualização Manual
1. Abra o programa RelatorioTJMS.exe
2. Clique no botão "🔄 Verificar Atualizações" (canto superior direito)
3. Se houver uma nova versão, clique "Sim" para atualizar
4. O programa será fechado e reaberto automaticamente

### Atualização Automática
- O programa verifica automaticamente por atualizações ao iniciar (modo silencioso)
- Se encontrar uma nova versão, mostra uma notificação discreta

## 🔧 Para Desenvolvedores

### Workflow de Desenvolvimento

1. **Fazer alterações no código**
```bash
# Editar arquivos: main_exe.py, config.py, etc.
```

2. **Testar localmente**
```bash
python build_exe.py
# Testar o executável em dist/RelatorioTJMS.exe
```

3. **Commit e push**
```bash
git add .
git commit -m "Melhoria no sistema de relatórios"
git push origin master
```

4. **GitHub Actions automaticamente:**
   - ✅ Executa build do executável
   - ✅ Cria nova release
   - ✅ Disponibiliza para download

### Build Manual (Desenvolvimento)
```bash
# Instalar dependências
pip install -r requirements.txt

# Compilar executável
python build_exe.py

# Executável será criado em: dist/RelatorioTJMS.exe
```

### Trigger Manual do Build
Se precisar forçar um novo build sem fazer alterações:

```bash
# Via interface web do GitHub:
# Actions → Build and Release EXE → Run workflow

# Ou criar um commit vazio:
git commit --allow-empty -m "Força novo build"
git push origin master
```

## 📦 Estrutura dos Arquivos

```
projeto/
├── .github/workflows/
│   └── build-release.yml      # GitHub Actions workflow
├── main_exe.py               # Aplicação principal
├── updater.py                # Módulo de auto-atualização
├── build_exe.py              # Script de build
├── config.py                 # Configurações
├── requirements.txt          # Dependências Python
└── dist/                     # Executável gerado
    ├── RelatorioTJMS.exe
    └── VERSION               # Arquivo de versão
```

## 🐛 Troubleshooting

### Problema: Build falha no GitHub Actions
**Solução:**
1. Verifique se `config.py` está configurado corretamente
2. Verifique se todas as dependências estão em `requirements.txt`
3. Veja os logs em Actions → Build and Release EXE

### Problema: Auto-update não funciona
**Solução:**
1. Verifique conexão com internet
2. Certifique-se que há uma release no GitHub
3. Verifique se o arquivo `updater.py` está incluído no executável

### Problema: Executável não abre após atualização
**Solução:**
1. Baixe manualmente a versão mais recente do GitHub Releases
2. Substitua o executável antigo
3. Execute como Administrador se necessário

## 📊 Monitoramento

### Ver Versão Atual
- No programa: aparece no título da janela
- Arquivo `VERSION` (se existir) contém a versão

### Ver Releases Disponíveis
- GitHub: https://github.com/kaoyeoshiro/AJG/releases
- API: `https://api.github.com/repos/kaoyeoshiro/AJG/releases/latest`

## 🎯 Próximos Passos

- [ ] Notificações de atualização mais discretas
- [ ] Changelog automático nas releases
- [ ] Rollback para versão anterior
- [ ] Atualizações incrementais (delta updates)

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas alterações
4. Push para a branch
5. Abra um Pull Request

O sistema de build automático funcionará em forks também, facilitando o desenvolvimento colaborativo.

---

## 📞 Suporte

Para problemas relacionados ao sistema de auto-atualização:
- Abra uma issue no GitHub: https://github.com/kaoyeoshiro/AJG/issues
- Verifique os logs do GitHub Actions
- Teste a versão mais recente disponível

🎉 **Aproveite o sistema de atualizações automáticas!**