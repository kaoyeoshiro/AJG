#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair automaticamente os IDs corretos dos campos do Google Forms
"""

import requests
import re
import os
from dotenv import load_dotenv

def extract_form_ids():
    load_dotenv()
    
    url = os.getenv('GOOGLE_FORM_URL', '')
    
    if not url:
        print('❌ GOOGLE_FORM_URL não configurada no .env')
        return False
    
    # Converter para URL de visualização
    view_url = url.replace('/formResponse', '/viewform')
    print(f'🔗 Acessando: {view_url}')
    
    try:
        # Buscar o HTML do formulário
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(view_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f'❌ Erro ao acessar formulário: {response.status_code}')
            return False
        
        html = response.text
        print(f'✅ HTML obtido ({len(html)} caracteres)')
        
        # Extrair todos os campos entry.*
        pattern = r'name="(entry\.\d+)"'
        matches = re.findall(pattern, html)
        
        if not matches:
            print('❌ Nenhum campo entry.* encontrado no HTML')
            # Tentar outro padrão
            pattern2 = r'"entry\.(\d+)"'
            matches2 = re.findall(pattern2, html)
            if matches2:
                matches = [f'entry.{m}' for m in matches2]
                print(f'✅ Encontrados {len(matches)} campos com padrão alternativo')
            else:
                print('❌ Nenhum campo encontrado com padrões alternativos')
                return False
        else:
            print(f'✅ Encontrados {len(matches)} campos entry.*')
        
        # Remover duplicatas mantendo ordem
        unique_entries = []
        for entry in matches:
            if entry not in unique_entries:
                unique_entries.append(entry)
        
        print(f'\n📋 IDs dos campos encontrados:')
        for i, entry in enumerate(unique_entries, 1):
            print(f'  Campo {i}: {entry}')
        
        if len(unique_entries) >= 5:
            print('\n🎯 CONFIGURAÇÃO SUGERIDA PARA O .env:')
            print(f'GOOGLE_FORM_FIELD_TIPO={unique_entries[0]}')
            print(f'GOOGLE_FORM_FIELD_DESCRICAO={unique_entries[1]}')
            print(f'GOOGLE_FORM_FIELD_PROCESSO={unique_entries[2]}')
            print(f'GOOGLE_FORM_FIELD_MODELO={unique_entries[3]}')
            print(f'GOOGLE_FORM_FIELD_TIMESTAMP={unique_entries[4]}')
            
            if len(unique_entries) > 5:
                print(f'# CAMPO EXTRA: {unique_entries[5]} (se necessário)')
        else:
            print(f'\n⚠️  Apenas {len(unique_entries)} campos encontrados. Esperados: 5')
        
        # Tentar identificar os tipos de campos
        print('\n🔍 Analisando tipos de campos...')
        
        # Buscar por labels/títulos dos campos
        label_patterns = [
            r'aria-label="([^"]*)"[^>]*name="' + re.escape(entry) + '"',
            r'"' + re.escape(entry) + '"[^>]*aria-label="([^"]*)"',
        ]
        
        for i, entry in enumerate(unique_entries[:5]):
            print(f'  {entry}:', end=' ')
            
            found_label = False
            for pattern in label_patterns:
                label_matches = re.findall(pattern, html, re.IGNORECASE)
                if label_matches:
                    print(f'"{label_matches[0]}"')
                    found_label = True
                    break
            
            if not found_label:
                # Buscar contexto ao redor do campo
                context_pattern = r'.{0,100}' + re.escape(entry) + r'.{0,100}'
                context_match = re.search(context_pattern, html)
                if context_match:
                    context = context_match.group(0)
                    # Limpar HTML tags
                    context_clean = re.sub(r'<[^>]+>', ' ', context)
                    context_clean = re.sub(r'\s+', ' ', context_clean).strip()
                    print(f'Contexto: {context_clean[:80]}...')
                else:
                    print('(tipo não identificado)')
        
        return True
        
    except Exception as e:
        print(f'❌ Erro ao extrair IDs: {e}')
        return False

def test_with_extracted_ids():
    """Fazer teste rápido com os IDs mais prováveis"""
    print('\n🧪 TESTE COM IDs EXTRAÍDOS...')
    
    # IDs que acabamos de extrair (você pode ajustar manualmente)
    test_ids = [
        'entry.811378283',  # Tipo
        'entry.77871712',   # Descrição  
        'entry.72495185',   # Processo
        'entry.391250636',  # Modelo
        'entry.864187237'   # Timestamp
    ]
    
    print('Testando com os IDs atuais do .env...')
    
    # Fazer teste simples
    load_dotenv()
    url = os.getenv('GOOGLE_FORM_URL', '')
    
    if not url:
        print('❌ URL não configurada')
        return
    
    data = {
        test_ids[0]: 'TESTE_IDS',
        test_ids[1]: 'Teste com IDs extraídos automaticamente', 
        test_ids[2]: '0000000-00.2025.0.00.0000',
        test_ids[3]: 'script-automatico',
        test_ids[4]: '2025-09-12 08:30:00'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        print(f'Status: {response.status_code}')
        
        if response.status_code in [200, 302]:
            print('✅ TESTE FUNCIONOU! IDs estão corretos.')
        else:
            print('❌ Teste falhou. IDs podem estar incorretos.')
            
    except Exception as e:
        print(f'❌ Erro no teste: {e}')

if __name__ == '__main__':
    print('=== EXTRAÇÃO AUTOMÁTICA DE IDs DO GOOGLE FORMS ===\n')
    
    success = extract_form_ids()
    
    if success:
        test_with_extracted_ids()
    
    print('\n=== CONCLUÍDO ===')
