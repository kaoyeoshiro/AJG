# 🚀 Instruções para Criar Executável (.exe)

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Dependências do projeto** instaladas:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Passos para Gerar o Executável

### Passo 1: Configurar Credenciais
Edite o arquivo `config.py` e substitua os valores placeholder:

```python
# Substitua estes valores pelas suas credenciais reais:
TJ_WSDL_URL = "https://seu-tjms-wsdl-url"
TJ_WS_USER = "seu_usuario"
TJ_WS_PASS = "sua_senha"
OPENROUTER_API_KEY = "sk-or-v1-sua-chave-aqui"
```

### Passo 2: Executar o Build
```bash
python build_exe.py
```

Este comando irá:
- ✅ Verificar se as configurações foram preenchidas
- 📦 Instalar PyInstaller automaticamente se necessário
- 🔨 Compilar o executável
- 📁 Criar o arquivo `dist/RelatorioTJMS.exe`

## 📁 Arquivos Gerados

Após o build bem-sucedido:
```
dist/
└── RelatorioTJMS.exe    # ← Executável final (distribuir este arquivo)

build/                   # Arquivos temporários (pode deletar)
RelatorioTJMS.spec      # Configuração do PyInstaller
```

## 🧪 Testar o Executável

1. **Teste local:**
   ```bash
   dist/RelatorioTJMS.exe
   ```

2. **Teste em máquina limpa:**
   - Copie apenas `RelatorioTJMS.exe` para outro computador
   - Execute com duplo clique
   - Teste todas as funcionalidades

## 🔍 Solução de Problemas

### Erro: "Configurações não preenchidas"
- Verifique se editou corretamente o `config.py`
- Certifique-se de não ter deixado valores como `"SEU_*_AQUI"`

### Erro: "PyInstaller não encontrado"
```bash
pip install pyinstaller
```

### Executável muito grande
- Normal para aplicações Python (20-50MB)
- O PyInstaller embute o interpretador Python

### Antivírus bloqueia o executável
- Normal para executáveis gerados pelo PyInstaller
- Adicione exceção no antivírus ou assine digitalmente

## ⚙️ Personalizações Avançadas

Para modificar o build, edite `build_exe.py`:

```python
# Adicionar ícone
icon='icon.ico'

# Habilitar console (para debug)
console=True

# Excluir módulos desnecessários
excludes=['numpy', 'matplotlib']
```

## 📦 Distribuição

O executável final (`RelatorioTJMS.exe`) é **standalone** e contém:
- ✅ Todas as dependências Python
- ✅ Configurações embutidas
- ✅ Interface gráfica Tkinter
- ❌ Não precisa de instalação do Python
- ❌ Não precisa de arquivo .env

## 🎯 Comandos Resumidos

```bash
# 1. Configurar credenciais
# Editar config.py manualmente

# 2. Gerar executável
python build_exe.py

# 3. Testar
dist/RelatorioTJMS.exe

# 4. Distribuir
# Copiar apenas o arquivo dist/RelatorioTJMS.exe
```