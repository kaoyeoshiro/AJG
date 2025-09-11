# Templates para Relatórios

Esta pasta contém templates para geração de relatórios em DOCX e PDF com cabeçalho e rodapé personalizados.

## Como Funciona

O sistema detecta automaticamente templates e usa-os:
1. **Você cria um template DOCX** com cabeçalho, rodapé e estilos
2. **O sistema insere o relatório** usando os estilos do template
3. **PDF é gerado** convertendo o DOCX final

## Arquivos de Template

### Para DOCX (Recomendado)
Crie o arquivo: **`template.docx`**
- ✅ **Abra o Word** ou LibreOffice Writer
- ✅ **Configure cabeçalho e rodapé** com logos e informações
- ✅ **Defina estilos** (Título 1, Título 2, Normal, etc.)
- ✅ **Salve como template.docx** nesta pasta

### Para RTF (Descontinuado)
O suporte a RTF foi removido. Use DOCX.

## Exemplo de Template DOCX

Abra o Word e configure:

```
📄 template.docx
┌─────────────────────────────┐
│ CABEÇALHO                   │
│ [Logo da Instituição]       │
│ Tribunal de Justiça - MS    │
├─────────────────────────────┤
│                             │
│  (Documento será inserido)  │ 
│   ← Conteúdo automático ←   │
│                             │
├─────────────────────────────┤
│ RODAPÉ                      │
│ Gerado automaticamente     │
│ Página {PAGE}               │
└─────────────────────────────┘
```

## Como Criar o Template DOCX

1. **Abra o Microsoft Word** ou LibreOffice Writer
2. **Configure cabeçalho:**
   - Inserir > Cabeçalho > Editar cabeçalho
   - Adicione logo, título, etc.
3. **Configure rodapé:**
   - Inserir > Rodapé > Editar rodapé  
   - Adicione informações, número de página
4. **Configure estilos:**
   - Título 1: Para cabeçalhos principais (#)
   - Título 2: Para subcabeçalhos (##)
   - Normal: Para texto comum
5. **Salve como:** `templates/template.docx`

## Conversão para PDF

- **Melhor opção:** LibreOffice instalado (conversão perfeita)
- **Alternativa:** `pip install docx2pdf` (boa qualidade)
- **Sem dependências:** Apenas DOCX (compatível com tudo)

## Instalação para PDF

**Windows/Mac:**
```
pip install docx2pdf
```

**Linux:**
```
sudo apt install libreoffice
# OU
pip install docx2pdf
```
