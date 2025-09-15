#!/usr/bin/env python3
"""
Script completo para testar e corrigir envio ao Google Forms
Identifica causas do erro 400 e fornece solução funcional
VERSÃO CORRIGIDA baseada nos IDs reais encontrados
"""
import os
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, Optional, Tuple

class GoogleFormsDebugger:
    def __init__(self):
        # Configurações do formulário
        self.form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/formResponse"
        self.view_url = "https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/viewform"

        # IDs dos campos CORRIGIDOS baseados na análise do console
        self.fields = {
            "TIPO": "entry.1930801017",        # Campo de múltipla escolha
            "DESCRICAO": "entry.811378283",    # Texto longo
            "PROCESSO": "entry.77871712",      # Texto curto  
            "MODELO": "entry.72495185",        # Texto curto
            "TIMESTAMP": "entry.864187237"     # Texto curto
        }

        # Headers apropriados para Google Forms
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://docs.google.com',
            'Referer': self.view_url,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def debug_response(self, response: requests.Response) -> Dict:
        """Captura informações detalhadas da resposta"""
        debug_info = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'url': response.url,
            'content_length': len(response.content),
            'content_preview': response.text[:500],
            'redirects': len(response.history),
            'final_url': response.url
        }

        # Detecta redirecionamentos
        if response.history:
            debug_info['redirect_chain'] = [r.url for r in response.history]

        # Verifica se foi para página de confirmação (sucesso é 200 + redirect)
        if response.status_code == 200:
            debug_info['success'] = True
        else:
            debug_info['success'] = False

        return debug_info

    def test_method_1_with_sentinel(self) -> Tuple[bool, Dict]:
        """Teste 1: POST com campo sentinel para múltipla escolha"""
        print("TESTE 1: POST com campo sentinel...")

        data = {
            "entry.1930801017_sentinel": "",  # Campo sentinel vazio
            self.fields["TIPO"]: "ERRO",       # Valor da múltipla escolha
            self.fields["DESCRICAO"]: "Teste com campo sentinel",
            self.fields["PROCESSO"]: "123456789",
            self.fields["MODELO"]: "MODELO_TESTE_1",
            self.fields["TIMESTAMP"]: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            response = requests.post(
                self.form_url,
                data=data,
                headers=self.headers,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_2_without_tipo(self) -> Tuple[bool, Dict]:
        """Teste 2: POST sem o campo problemático de múltipla escolha"""
        print("TESTE 2: POST sem campo TIPO...")

        data = {
            self.fields["DESCRICAO"]: "Teste sem campo tipo",
            self.fields["PROCESSO"]: "987654321",
            self.fields["MODELO"]: "MODELO_TESTE_2",
            self.fields["TIMESTAMP"]: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            response = requests.post(
                self.form_url,
                data=data,
                headers=self.headers,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_3_simple_tipo(self) -> Tuple[bool, Dict]:
        """Teste 3: POST apenas com campo TIPO simples"""
        print("TESTE 3: POST so com campo TIPO...")

        data = {
            self.fields["TIPO"]: "SUCESSO_AUTO"
        }

        try:
            response = requests.post(
                self.form_url,
                data=data,
                headers=self.headers,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_4_basic_values(self) -> Tuple[bool, Dict]:
        """Teste 4: POST com valores básicos e corretos"""
        print("TESTE 4: POST com valores basicos...")

        data = {
            self.fields["TIPO"]: "ERRO",
            self.fields["DESCRICAO"]: "teste",
            self.fields["PROCESSO"]: "123456789",
            self.fields["MODELO"]: "gpt-4",
            self.fields["TIMESTAMP"]: "2025-09-13"
        }

        try:
            response = requests.post(
                self.form_url,
                data=data,
                headers=self.headers,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_5_minimal_headers(self) -> Tuple[bool, Dict]:
        """Teste 5: Headers mínimos"""
        print("TESTE 5: Headers minimos...")

        minimal_headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            self.fields["TIPO"]: "ERRO",
            self.fields["DESCRICAO"]: "teste minimal"
        }

        try:
            response = requests.post(
                self.form_url,
                data=data,
                headers=minimal_headers,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_6_session_cookies(self) -> Tuple[bool, Dict]:
        """Teste 6: Com sessão e cookies do Google"""
        print("TESTE 6: Com sessao e cookies...")

        session = requests.Session()
        
        try:
            # Primeiro visita a página do formulário para obter cookies
            session.get(self.view_url, headers=self.headers, timeout=15)
            
            data = {
                "entry.1930801017": "ERRO",
                "entry.811378283": "Teste com sessao",
                "entry.77871712": "555666777",
                "entry.72495185": "modelo_sessao",
                "entry.864187237": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            response = session.post(
                self.form_url,
                data=data,
                headers=self.headers,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_7_url_encoded_values(self) -> Tuple[bool, Dict]:
        """Teste 7: Com valores URL encoded"""
        print("TESTE 7: Com valores URL encoded...")

        data = {
            "entry.1930801017": "SUCESSO_AUTO",
            "entry.811378283": urllib.parse.quote("Teste com caracteres especiais: ção, ã, é"),
            "entry.77871712": "1234567-89.2020.1.23.4567",
            "entry.72495185": urllib.parse.quote("openai/gpt-4o-mini"),
            "entry.864187237": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            response = requests.post(
                self.form_url,
                data=data,
                headers=self.headers,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_8_different_user_agents(self) -> Tuple[bool, Dict]:
        """Teste 8: Com diferentes User-Agents"""
        print("TESTE 8: Com User-Agent diferente...")

        headers_alt = self.headers.copy()
        headers_alt['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

        data = {
            "entry.1930801017": "ERRO",
            "entry.811378283": "Teste User-Agent Linux",
            "entry.77871712": "999888777",
            "entry.72495185": "claude-3",
            "entry.864187237": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            response = requests.post(
                self.form_url,
                data=data,
                headers=headers_alt,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_9_with_additional_headers(self) -> Tuple[bool, Dict]:
        """Teste 9: Com headers adicionais"""
        print("TESTE 9: Com headers adicionais...")

        headers_extra = self.headers.copy()
        headers_extra.update({
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin'
        })

        data = {
            "entry.1930801017": "SUCESSO_AUTO",
            "entry.811378283": "Teste headers extras",
            "entry.77871712": "444555666",
            "entry.72495185": "gemini-pro",
            "entry.864187237": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            response = requests.post(
                self.form_url,
                data=data,
                headers=headers_extra,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def test_method_10_with_form_tokens(self) -> Tuple[bool, Dict]:
        """Teste 10: Tentando capturar e usar tokens do formulário"""
        print("TESTE 10: Com tokens do formulario...")

        session = requests.Session()
        
        try:
            # Obtém a página do formulário
            form_response = session.get(self.view_url, headers=self.headers, timeout=15)
            
            # Tenta extrair tokens/campos hidden da página
            import re
            
            # Procura por campos hidden que podem ser necessários
            hidden_fields = {}
            for match in re.finditer(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\'][^>]*>', form_response.text):
                field_name = match.group(1)
                field_value = match.group(2)
                if field_name not in ['fbzx', 'fvv', 'partialResponse', 'pageHistory', 'submissionTimestamp']:
                    hidden_fields[field_name] = field_value
            
            print(f"   Campos hidden encontrados: {list(hidden_fields.keys())}")
            
            data = {
                "entry.1930801017": "ERRO",
                "entry.811378283": "Teste com tokens",
                "entry.77871712": "777888999",
                "entry.72495185": "modelo_token",
                "entry.864187237": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Adiciona campos hidden encontrados
            data.update(hidden_fields)

            response = session.post(
                self.form_url,
                data=data,
                headers=self.headers,
                timeout=30,
                allow_redirects=True
            )

            debug_info = self.debug_response(response)
            print(f"   Status: {response.status_code}")
            print(f"   Success: {debug_info['success']}")

            return debug_info['success'], debug_info

        except Exception as e:
            return False, {'error': str(e)}

    def run_progressive_tests(self) -> Dict:
        """Executa testes progressivos até encontrar 100% de sucesso"""
        print("=" * 60)
        print("TESTE COMPLETO - BUSCANDO 100% DE SUCESSO")
        print("=" * 60)
        print(f"URL do formulario: {self.form_url}")
        print(f"URL de visualizacao: {self.view_url}")
        print()
        print("IDs dos campos confirmados:")
        for name, entry_id in self.fields.items():
            print(f"  {name}: {entry_id}")
        print()

        results = {}
        all_tests = [
            ('with_sentinel', self.test_method_1_with_sentinel),
            ('without_tipo', self.test_method_2_without_tipo),
            ('only_tipo', self.test_method_3_simple_tipo),
            ('basic_values', self.test_method_4_basic_values),
            ('minimal_headers', self.test_method_5_minimal_headers),
            ('session_cookies', self.test_method_6_session_cookies),
            ('url_encoded', self.test_method_7_url_encoded_values),
            ('different_ua', self.test_method_8_different_user_agents),
            ('extra_headers', self.test_method_9_with_additional_headers),
            ('form_tokens', self.test_method_10_with_form_tokens)
        ]

        # Executa todos os testes
        for test_name, test_method in all_tests:
            success, info = test_method()
            results[test_name] = {'success': success, 'info': info}
            print()

        # Análise dos resultados
        self.analyze_results(results)

        return results

    def analyze_results(self, results: Dict):
        """Analisa resultados e fornece recomendações"""
        print("=" * 60)
        print("ANALISE DOS RESULTADOS")
        print("=" * 60)

        successful_methods = []

        for method_name, result in results.items():
            if result['success']:
                successful_methods.append(method_name)
                print(f"✅ SUCCESS {method_name.upper()}: FUNCIONOU")
            else:
                print(f"❌ FAIL {method_name.upper()}: FALHOU")
                if 'error' in result['info']:
                    print(f"   Erro: {result['info']['error']}")
                else:
                    status = result['info'].get('status_code', 'N/A')
                    print(f"   Status: {status}")
                    if status == 400:
                        print(f"   Preview: {result['info'].get('content_preview', '')[:100]}")

        print()
        print("RECOMENDACOES:")

        if successful_methods:
            print(f"✅ Metodo funcional encontrado: {successful_methods[0].upper()}")
            self.generate_working_code(successful_methods[0])
        else:
            print("❌ Nenhum metodo funcionou. Investigacoes adicionais:")
            print("   1. Verifique se o formulario aceita respostas")
            print("   2. Teste preenchimento manual no navegador")
            print("   3. Confirme IDs dos campos com JavaScript no console")
            print("   4. Verifique se ha restricoes de CORS ou reCAPTCHA")

    def generate_working_code(self, method: str):
        """Gera código Python funcional baseado no método que funcionou"""
        print()
        print("=" * 60)
        print("CODIGO PYTHON FUNCIONAL PARA SEU SISTEMA")
        print("=" * 60)

        if method == 'with_sentinel':
            code = '''
def send_feedback_to_google_forms(tipo: str, descricao: str, processo: str, modelo: str) -> bool:
    """
    Envia feedback para Google Forms - MÉTODO COM SENTINEL
    
    Args:
        tipo: "ERRO" ou "SUCESSO_AUTO"
        descricao: Descrição do problema/sucesso
        processo: Número do processo CNJ
        modelo: Modelo LLM utilizado
    
    Returns:
        bool: True se enviado com sucesso
    """
    import requests
    from datetime import datetime
    
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/formResponse"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://docs.google.com',
        'Referer': 'https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/viewform'
    }
    
    data = {
        "entry.1930801017_sentinel": "",     # Campo sentinel obrigatório
        "entry.1930801017": tipo,            # TIPO: ERRO ou SUCESSO_AUTO
        "entry.811378283": descricao,        # DESCRIÇÃO
        "entry.77871712": processo,          # PROCESSO CNJ
        "entry.72495185": modelo,            # MODELO LLM
        "entry.864187237": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # TIMESTAMP
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar feedback: {e}")
        return False

# SUBSTITUA sua função atual por esta:
# Em vez de:
# data = {
#     os.getenv("GOOGLE_FORM_FIELD_TIPO"): tipo,
#     os.getenv("GOOGLE_FORM_FIELD_DESCRICAO"): descricao,
#     ...
# }
#
# Use:
success = send_feedback_to_google_forms(
    tipo=tipo,           # Sua variável
    descricao=descricao, # Sua variável  
    processo=processo,   # Sua variável
    modelo=modelo        # Sua variável
)
'''

        elif method == 'without_tipo':
            code = '''
def send_feedback_to_google_forms(descricao: str, processo: str, modelo: str) -> bool:
    """
    Envia feedback SEM o campo TIPO (que estava causando problema)
    """
    import requests
    from datetime import datetime
    
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/formResponse"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        "entry.811378283": descricao,
        "entry.77871712": processo,
        "entry.72495185": modelo,
        "entry.864187237": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False
'''

        elif method == 'basic_values':
            code = '''
def send_feedback_to_google_forms(tipo: str, descricao: str, processo: str, modelo: str) -> bool:
    """
    Envia feedback com valores básicos - MÉTODO FUNCIONAL
    """
    import requests
    from datetime import datetime
    
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/formResponse"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        "entry.1930801017": tipo,            # ERRO ou SUCESSO_AUTO
        "entry.811378283": descricao,        # Texto da descrição
        "entry.77871712": processo,          # Número do processo
        "entry.72495185": modelo,            # Nome do modelo
        "entry.864187237": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False
'''

        print(code)
        print()
        print("COMO INTEGRAR NO SEU CÓDIGO:")
        print("1. Substitua a estrutura atual de envio pela função acima")
        print("2. Remova as variáveis do .env relacionadas aos campos")
        print("3. Use IDs fixos (já funcionais)")
        print("4. Teste com dados reais")

def main():
    """Função principal para executar os testes"""
    debugger = GoogleFormsDebugger()
    results = debugger.run_progressive_tests()
    return results

if __name__ == "__main__":
    main()