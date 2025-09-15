#!/usr/bin/env python3
"""
Script para extrair IDs corretos dos campos do Google Forms
e identificar a causa exata do erro 400
"""
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def extract_form_details():
    """Extrai detalhes completos do formulário Google Forms"""

    # URL para visualização do formulário
    view_url = "https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/viewform"

    # Headers para parecer um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none'
    }

    print("=" * 70)
    print("ANALISANDO FORMULARIO GOOGLE FORMS")
    print("=" * 70)
    print(f"URL: {view_url}")
    print()

    try:
        # Fazer request para obter o HTML do formulário
        print("Fazendo request para o formulario...")
        response = requests.get(view_url, headers=headers, timeout=30)

        print(f"Status Code: {response.status_code}")
        print(f"Content-Length: {len(response.content)}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        print()

        if response.status_code != 200:
            print(f"ERRO: Status {response.status_code}")
            print("Resposta:")
            print(response.text[:1000])
            return None

        # Parse do HTML
        print("Analisando HTML...")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar todos os campos de entrada (entry.*)
        entry_fields = []

        # Método 1: Buscar por name="entry.*"
        inputs_by_name = soup.find_all('input', {'name': re.compile(r'^entry\.\d+$')})
        textareas_by_name = soup.find_all('textarea', {'name': re.compile(r'^entry\.\d+$')})

        for element in inputs_by_name + textareas_by_name:
            name = element.get('name')
            field_type = element.get('type', element.name)
            aria_label = element.get('aria-label', '')
            data_params = element.get('data-params', '')

            entry_fields.append({
                'name': name,
                'type': field_type,
                'label': aria_label,
                'element': element.name,
                'data_params': data_params
            })

        # Método 2: Buscar por padrões no HTML
        entry_pattern = r'entry\.(\d+)'
        entries_in_html = re.findall(entry_pattern, response.text)
        entries_in_html = list(set(entries_in_html))  # Remove duplicatas

        print(f"Campos encontrados por name attribute: {len(entry_fields)}")
        print(f"Entry IDs encontrados no HTML: {len(entries_in_html)}")
        print()

        # Exibir campos encontrados
        if entry_fields:
            print("CAMPOS ENCONTRADOS:")
            print("-" * 50)
            for i, field in enumerate(entry_fields, 1):
                print(f"{i}. Nome: {field['name']}")
                print(f"   Tipo: {field['type']}")
                print(f"   Label: {field['label'][:100]}...")
                print(f"   Elemento: <{field['element']}>")
                print()
        else:
            print("NENHUM CAMPO ENCONTRADO POR NAME ATTRIBUTE")
            print()

        # Exibir todos os entry IDs encontrados
        if entries_in_html:
            print("TODOS OS ENTRY IDs NO HTML:")
            print("-" * 30)
            for entry_id in sorted(entries_in_html):
                print(f"entry.{entry_id}")
            print()

        # Buscar o action do formulário
        forms = soup.find_all('form')
        print(f"Formularios encontrados: {len(forms)}")

        for i, form in enumerate(forms):
            action = form.get('action', 'N/A')
            method = form.get('method', 'N/A')
            print(f"Form {i+1}: action='{action}', method='{method}'")
        print()

        # Buscar informações específicas sobre o formulário
        form_data = extract_form_metadata(response.text)

        if form_data:
            print("METADADOS DO FORMULARIO:")
            print("-" * 30)
            for key, value in form_data.items():
                print(f"{key}: {value}")
            print()

        # Tentar extrair a estrutura de perguntas
        questions = extract_questions_structure(soup)

        if questions:
            print("ESTRUTURA DAS PERGUNTAS:")
            print("-" * 40)
            for i, q in enumerate(questions, 1):
                print(f"{i}. {q['title'][:80]}...")
                print(f"   Entry: {q.get('entry', 'N/A')}")
                print(f"   Tipo: {q.get('type', 'N/A')}")
                print()

        return {
            'entry_fields': entry_fields,
            'entries_in_html': entries_in_html,
            'forms': [(f.get('action'), f.get('method')) for f in forms],
            'form_metadata': form_data,
            'questions': questions,
            'html_content': response.text
        }

    except Exception as e:
        print(f"ERRO ao analisar formulario: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_form_metadata(html_content):
    """Extrai metadados do formulário do JavaScript"""
    metadata = {}

    # Buscar por padrões comuns no JavaScript
    patterns = {
        'form_id': r'"FB_PUBLIC_LOAD_DATA_",\s*\[null,\[null,null,null,\[.*?"([^"]*)"',
        'form_response_url': r'"([^"]*formResponse[^"]*)"',
        'form_view_url': r'"([^"]*viewform[^"]*)"'
    }

    for key, pattern in patterns.items():
        matches = re.findall(pattern, html_content)
        if matches:
            metadata[key] = matches[0] if len(matches) == 1 else matches

    return metadata

def extract_questions_structure(soup):
    """Tenta extrair a estrutura das perguntas do formulário"""
    questions = []

    # Buscar por elementos que contêm perguntas
    question_elements = soup.find_all('div', {'data-params': re.compile(r'.*entry\.\d+.*')})

    for element in question_elements:
        try:
            # Extrair título da pergunta
            title_element = element.find('span', class_=re.compile(r'.*question.*'))
            title = title_element.get_text(strip=True) if title_element else "Título não encontrado"

            # Extrair entry ID
            data_params = element.get('data-params', '')
            entry_match = re.search(r'entry\.(\d+)', data_params)
            entry = f"entry.{entry_match.group(1)}" if entry_match else None

            # Tentar identificar o tipo de campo
            field_type = "unknown"
            if element.find('input', {'type': 'text'}):
                field_type = "text"
            elif element.find('textarea'):
                field_type = "textarea"
            elif element.find('input', {'type': 'radio'}):
                field_type = "radio"
            elif element.find('select'):
                field_type = "select"

            questions.append({
                'title': title,
                'entry': entry,
                'type': field_type,
                'data_params': data_params
            })

        except Exception as e:
            continue

    return questions

def test_specific_entries():
    """Testa os entry IDs que você forneceu especificamente"""
    print("=" * 70)
    print("TESTANDO ENTRY IDs FORNECIDOS")
    print("=" * 70)

    # IDs fornecidos pelo usuário
    provided_entries = {
        "TIPO": "entry.1930801017",
        "DESCRICAO": "entry.811378283",
        "PROCESSO": "entry.77871712",
        "MODELO": "entry.72495185",
        "TIMESTAMP": "entry.864187237"
    }

    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/formResponse"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://docs.google.com',
        'Referer': 'https://docs.google.com/forms/d/e/1FAIpQLSdnbKWxgHAzaQC-RhnsSG7ojfIXz25UkaWv0xKRhMwkT0qz7A/viewform'
    }

    # Teste com apenas um campo por vez
    for field_name, entry_id in provided_entries.items():
        print(f"Testando {field_name} ({entry_id})...")

        data = {entry_id: "TESTE"}

        try:
            response = requests.post(form_url, data=data, headers=headers, timeout=15, allow_redirects=True)
            print(f"  Status: {response.status_code}")

            if response.status_code == 200 and 'formResponse' in response.url:
                print(f"  SUCESSO: {field_name} funciona!")
            else:
                print(f"  FALHA: Status {response.status_code}")
                if response.status_code == 400:
                    print(f"    Resposta: {response.text[:200]}...")

        except Exception as e:
            print(f"  ERRO: {e}")

        print()

def main():
    """Função principal"""
    # Primeiro, extrair informações do formulário
    form_info = extract_form_details()

    print("=" * 70)

    # Depois, testar os IDs fornecidos
    test_specific_entries()

    # Resumo final
    print("=" * 70)
    print("RESUMO E PROXIMO PASSO:")
    print("-" * 30)

    if form_info and form_info['entry_fields']:
        print("1. IDs encontrados no HTML do formulario:")
        for field in form_info['entry_fields']:
            print(f"   {field['name']} - {field['label'][:50]}...")

    print("\n2. Proximos passos:")
    print("   - Compare os IDs fornecidos com os encontrados no HTML")
    print("   - Se diferentes, use os IDs corretos do HTML")
    print("   - Se iguais, o problema pode ser de headers ou método")

    return form_info

if __name__ == "__main__":
    main()