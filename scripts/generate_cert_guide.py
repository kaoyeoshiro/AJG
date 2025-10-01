#!/usr/bin/env python3
"""
Script para gerar guia de configuração de certificado digital
para assinatura de código (code signing)
"""

def generate_certificate_guide():
    guide = """
# 🔐 Guia de Configuração - Assinatura Digital

## Para Desenvolvedores/Mantenedores

### 1. Obter Certificado de Code Signing

#### Opções Comerciais (Recomendado):
- **DigiCert:** $200-400/ano - Mais confiável
- **Sectigo:** $150-300/ano - Boa relação custo/benefício
- **GlobalSign:** $200-350/ano - Amplamente aceito
- **SSL.com:** $100-250/ano - Mais barato

#### Requisitos:
- Validação de identidade (pessoa física ou jurídica)
- Documentos de identificação
- Processo de verificação (2-7 dias)

### 2. Preparar Certificado para GitHub

#### Converter para Base64:
```powershell
# Se o certificado é .pfx/.p12
$cert_bytes = [System.IO.File]::ReadAllBytes("certificado.p12")
$cert_base64 = [System.Convert]::ToBase64String($cert_bytes)
$cert_base64 | Out-File "certificado_base64.txt"
```

#### Configurar Secrets no GitHub:
1. Vá em **Settings** → **Secrets and variables** → **Actions**
2. Adicione **New repository secret**:
   - `CERTIFICATE_BASE64`: Cole o conteúdo do arquivo certificado_base64.txt
   - `CERTIFICATE_PASSWORD`: A senha do certificado .p12/.pfx

### 3. Verificar Assinatura

#### Após o build:
```powershell
# Verificar se está assinado
Get-AuthenticodeSignature AJG.exe

# Verificar detalhes
Get-AuthenticodeSignature AJG.exe | Format-List *
```

### 4. Alternativas Gratuitas (Limitadas)

#### Self-Signed Certificate (desenvolvimento):
```powershell
# Criar certificado auto-assinado (só para testes)
New-SelfSignedCertificate -DnsName "MeuApp" -Type CodeSigning -CertStoreLocation Cert:\\CurrentUser\\My
```
⚠️ **Nota:** Certificados auto-assinados NÃO são reconhecidos pelo Windows como confiáveis.

#### Certificados Gratuitos (Experimental):
- **SignPath.io:** Grátis para projetos open source
- **Azure Key Vault:** Parte do Azure (pode ter custos)

## Para Usuários Finais

### Como Verificar se um Executável está Assinado:

```powershell
Get-AuthenticodeSignature AJG.exe
```

**Status possíveis:**
- `Valid`: ✅ Assinatura válida e confiável
- `UnknownError`: ⚠️ Assinatura presente mas não reconhecida
- `NotSigned`: ❌ Arquivo não assinado

### Benefícios da Assinatura Digital:

1. **Reduz avisos do Windows Defender**
2. **Confirma autenticidade** do desenvolvedor
3. **Detecta modificações** no arquivo
4. **Aumenta confiança** dos usuários

---

## 💰 Custos vs Benefícios

### Sem Assinatura:
- ❌ Muitos avisos de segurança
- ❌ Usuários podem desconfiar
- ❌ Processo de download complicado
- ✅ Custo zero

### Com Assinatura:
- ✅ Menos avisos de segurança
- ✅ Maior confiança dos usuários
- ✅ Processo mais simples
- ❌ Custo anual ($100-400)

## 🎯 Recomendação

Para **projetos pessoais/pequenos:**
- Use build automatizado + checksums + documentação clara
- Instrua usuários sobre como adicionar exceções

Para **projetos comerciais/grandes:**
- Invista em certificado de code signing
- Processo vale o investimento em experiência do usuário

"""

    with open("CERTIFICADO_DIGITAL.md", "w", encoding="utf-8") as f:
        f.write(guide)

    print("Guia de certificado digital gerado: CERTIFICADO_DIGITAL.md")

if __name__ == "__main__":
    generate_certificate_guide()