# 📋 Prompt: Sistema de Templates para Geração de Documentos

> **Para uso em outro projeto**: Este documento explica como funciona o sistema de templates do projeto AJG (Assistência Judiciária Gratuita) para que você possa implementar funcionalidade similar.

---

## 🎯 Visão Geral do Sistema

O sistema permite gerar relatórios profissionais com **cabeçalho e rodapé personalizados** usando templates DOCX. O conteúdo é gerado em Markdown pela IA e então formatado usando o template do usuário.

### Fluxo de Trabalho

```
1. IA Gera Conteúdo (Markdown)
          ↓
2. Sistema Detecta Template
          ↓
3. Carrega template.docx (se existir)
          ↓
4. Insere Conteúdo no Template
          ↓
5. Exporta DOCX Final
          ↓
6. (Opcional) Converte para PDF
```

---

## 📁 Estrutura de Arquivos

```
projeto/
├── templates/
│   ├── template.docx      # Template com cabeçalho/rodapé (usuário cria)
│   └── README.md          # Instruções para o usuário
└── main_exe.py            # Código principal com função markdown_to_docx()
```

---

## 🔧 Implementação Técnica

### 1. Função Principal: `markdown_to_docx()`

**Localização**: `main_exe.py` linha ~1283

**Assinatura**:
```python
def markdown_to_docx(markdown_text: str, output_path: str, numero_processo: str = "") -> bool:
    """
    Converte markdown para DOCX usando python-docx com template se disponível

    Args:
        markdown_text: Conteúdo em Markdown gerado pela IA
        output_path: Caminho completo do arquivo DOCX de saída
        numero_processo: Número do processo (opcional, para título)

    Returns:
        True se sucesso, string com mensagem de erro se falhar
    """
```

### 2. Lógica de Detecção de Template

```python
# Tentar carregar template personalizado
template_path = os.path.join("templates", "template.docx")

if os.path.exists(template_path):
    try:
        doc = Document(template_path)  # Carrega template do usuário
        logger.info("Template DOCX carregado")

        # LIMPAR CONTEÚDO DO TEMPLATE (importante!)
        # Remove parágrafos existentes mas mantém cabeçalho/rodapé
        paragraphs_to_remove = []
        for paragraph in doc.paragraphs:
            paragraphs_to_remove.append(paragraph)

        for paragraph in paragraphs_to_remove:
            try:
                p = paragraph._element
                p.getparent().remove(p)
            except:
                pass  # Ignora erros

    except Exception as e:
        logger.warning(f"Erro ao carregar template: {e}. Usando documento em branco.")
        doc = Document()  # Fallback para documento vazio
else:
    # Se não existe template, cria documento em branco
    doc = Document()
```

### 3. Processamento de Markdown

O sistema processa markdown linha por linha e aplica formatação:

```python
lines = markdown_text.split('\n')

for line in lines:
    line = line.strip()

    # Cabeçalhos H3 (###)
    if line.startswith('### '):
        p = doc.add_paragraph()
        run = p.add_run(line[4:])  # Remove "### "
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 74, 107)  # Azul

    # Cabeçalhos H2 (##)
    elif line.startswith('## '):
        p = doc.add_paragraph()
        run = p.add_run(line[3:])  # Remove "## "
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 74, 107)

    # Cabeçalhos H1 (#)
    elif line.startswith('# '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(line[2:])  # Remove "# "
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(46, 74, 107)

    # Listas (-)
    elif line.startswith('- '):
        text = line[2:]
        list_counter += 1

        # Usar letras (a, b, c...)
        if list_counter <= 26:
            letter = chr(ord('a') + list_counter - 1)
            marker = f"{letter}) "
        else:
            marker = "• "

        p = doc.add_paragraph()
        p.add_run(marker)
        process_docx_inline_formatting(p, text)  # Processa **negrito**, *itálico*, etc.
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Texto normal
    else:
        p = doc.add_paragraph()
        process_docx_inline_formatting(p, line)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
```

### 4. Formatação Inline (Negrito, Itálico)

```python
def process_docx_inline_formatting(paragraph, text: str, base_italic: bool = False):
    """
    Processa formatação inline markdown e adiciona runs formatados ao parágrafo DOCX

    Suporta:
    - **negrito**
    - *itálico*
    - "citações"
    """
    i = 0
    current_text = ""

    while i < len(text):
        # Negrito **texto**
        if text[i:i+2] == '**':
            end_pos = text.find('**', i+2)
            if end_pos != -1:
                if current_text:
                    run = paragraph.add_run(current_text)
                    if base_italic:
                        run.italic = True
                    current_text = ""

                bold_text = text[i+2:end_pos]
                run = paragraph.add_run(bold_text)
                run.bold = True
                if base_italic:
                    run.italic = True

                i = end_pos + 2
                continue

        # Itálico *texto*
        elif text[i] == '*' and (i+1 < len(text) and text[i+1] != '*'):
            end_pos = text.find('*', i+1)
            if end_pos != -1:
                if current_text:
                    run = paragraph.add_run(current_text)
                    if base_italic:
                        run.italic = True
                    current_text = ""

                italic_text = text[i+1:end_pos]
                run = paragraph.add_run(italic_text)
                run.italic = True

                i = end_pos + 1
                continue

        # Citações "texto"
        elif text[i] == '"':
            end_pos = text.find('"', i+1)
            if end_pos != -1:
                if current_text:
                    run = paragraph.add_run(current_text)
                    if base_italic:
                        run.italic = True
                    current_text = ""

                quote_text = text[i:end_pos+1]
                run = paragraph.add_run(quote_text)
                run.italic = True

                i = end_pos + 1
                continue

        current_text += text[i]
        i += 1

    # Adicionar texto restante
    if current_text:
        run = paragraph.add_run(current_text)
        if base_italic:
            run.italic = True
```

### 5. Salvar Documento

```python
# Salvar documento final
doc.save(output_path)
logger.info("DOCX gerado com sucesso")
return True
```

---

## 📦 Dependências Necessárias

```python
# requirements.txt
python-docx>=0.8.11  # Para manipulação de arquivos DOCX

# Opcional para conversão PDF
docx2pdf>=0.1.8      # Windows/Mac
# OU
# sudo apt install libreoffice  # Linux (melhor qualidade)
```

---

## 🎨 Como o Template Funciona

### Estrutura do Template DOCX

O usuário cria `templates/template.docx` no Microsoft Word ou LibreOffice:

```
┌─────────────────────────────────────┐
│ CABEÇALHO (Header Section)         │
│                                     │
│  [Logo da Instituição]              │
│  TRIBUNAL DE JUSTIÇA - MS           │
│  Assistência Judiciária Gratuita   │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  CORPO DO DOCUMENTO                 │
│  (O sistema insere aqui)            │
│                                     │
│  ← Conteúdo gerado pela IA          │
│  ← Processado de Markdown           │
│  ← Com formatação aplicada          │
│                                     │
├─────────────────────────────────────┤
│ RODAPÉ (Footer Section)             │
│                                     │
│  Gerado automaticamente pelo sistema│
│  Data: 01/10/2025                   │
│  Página 1 de 3                      │
│                                     │
└─────────────────────────────────────┘
```

### O Que o Sistema Preserva

✅ **Cabeçalho**: Mantém logo, título, informações
✅ **Rodapé**: Mantém numeração de página, data
✅ **Estilos**: Usa os estilos definidos no template
✅ **Margens**: Respeita margens configuradas
✅ **Fonte padrão**: Mantém configuração do template

### O Que o Sistema Substitui

❌ **Conteúdo do corpo**: Remove todo texto existente
✅ **Insere novo conteúdo**: Processado do Markdown

---

## 🔄 Conversão para PDF (Opcional)

```python
def docx_to_pdf(docx_path: str, pdf_path: str) -> bool:
    """
    Converte DOCX para PDF usando LibreOffice ou docx2pdf
    """
    import subprocess

    # Opção 1: LibreOffice (melhor qualidade)
    try:
        output_dir = os.path.dirname(pdf_path)
        cmd = [
            "soffice", "--headless", "--convert-to", "pdf",
            "--outdir", output_dir, docx_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            # LibreOffice cria arquivo com nome baseado no DOCX
            docx_name = os.path.splitext(os.path.basename(docx_path))[0]
            generated_pdf = os.path.join(output_dir, docx_name + ".pdf")

            if os.path.exists(generated_pdf) and generated_pdf != pdf_path:
                os.rename(generated_pdf, pdf_path)

            logger.info("DOCX convertido para PDF com LibreOffice")
            return True

    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        logger.warning(f"LibreOffice não disponível: {e}")

    # Opção 2: python-docx2pdf (fallback)
    try:
        from docx2pdf import convert
        convert(docx_path, pdf_path)
        logger.info("DOCX convertido para PDF com docx2pdf")
        return True
    except ImportError:
        logger.warning("docx2pdf não instalado")
    except Exception as e:
        logger.warning(f"docx2pdf falhou: {e}")

    return "ERRO: Para conversão DOCX→PDF instale LibreOffice ou pip install docx2pdf"
```

---

## 📝 Exemplo de Uso Completo

```python
# 1. IA gera conteúdo em Markdown
markdown_content = """
# Relatório - Processo 1234567-89.2024.1.23.4567

## 1. Identificação das Partes

**Polo ativo:**
- **Maria da Silva**: Consta no sistema como beneficiária da justiça gratuita.

**Polo passivo:**
- **Banco X S.A.**: Não consta no sistema.

## 2. Decisões Proferidas

Decisão de 01/01/2024: "Defiro a gratuidade à parte autora."
"""

# 2. Chamar função de conversão
resultado = markdown_to_docx(
    markdown_text=markdown_content,
    output_path="relatorio_processo_123.docx",
    numero_processo="1234567-89.2024.1.23.4567"
)

# 3. Verificar resultado
if resultado == True:
    print("✅ DOCX gerado com sucesso!")

    # 4. (Opcional) Converter para PDF
    pdf_resultado = docx_to_pdf(
        "relatorio_processo_123.docx",
        "relatorio_processo_123.pdf"
    )

    if pdf_resultado == True:
        print("✅ PDF gerado com sucesso!")
else:
    print(f"❌ Erro: {resultado}")
```

---

## 🎯 Pontos-Chave para Implementação

### 1. **Limpeza do Template É Crítica**
- Remover todo conteúdo do corpo do documento
- Preservar cabeçalho e rodapé
- Manter configurações de estilo

### 2. **Processamento de Markdown Robusto**
- Suportar H1, H2, H3
- Processar listas com marcadores
- Formatação inline (negrito, itálico, citações)

### 3. **Fallback Inteligente**
- Se template não existe → criar documento em branco
- Se conversão PDF falha → manter DOCX
- Logging claro de cada etapa

### 4. **Experiência do Usuário**
- Detectar template automaticamente
- Não exigir configuração manual
- Funcionar sem template (modo padrão)

---

## ⚠️ Armadilhas Comuns

### ❌ Não Fazer:
1. **Não misturar RTF com DOCX** - são formatos incompatíveis
2. **Não processar HTML diretamente** - converter para Markdown primeiro
3. **Não assumir LibreOffice instalado** - ter fallbacks
4. **Não esquecer de limpar o template** - ficará com conteúdo duplicado

### ✅ Fazer:
1. **Testar sem template** - deve funcionar com documento vazio
2. **Validar encoding** - usar UTF-8 para caracteres especiais
3. **Logar cada etapa** - facilita debug
4. **Preservar formatação** - manter estrutura do Markdown

---

## 📚 Referências

- **python-docx**: https://python-docx.readthedocs.io/
- **Markdown Spec**: https://commonmark.org/
- **LibreOffice CLI**: https://wiki.documentfoundation.org/Documentation/HowTo/CommandLine

---

## 🔗 Código Fonte Completo

Veja a implementação completa em:
- `main_exe.py` linhas 1283-1426 (função `markdown_to_docx`)
- `main_exe.py` linhas 1565-1648 (função `process_docx_inline_formatting`)
- `main_exe.py` linhas 1669-1716 (função `docx_to_pdf`)

---

**Autor**: Sistema AJG - Assistência Judiciária Gratuita
**Versão**: 1.0.0
**Data**: 01/10/2025
**Licença**: Consulte LICENSE do repositório
