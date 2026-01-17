import pandas as pd
import re

# Seu link CSV do Google Sheets
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQu8BfHaCDnt0y0YZmLK0Ntdf9Jzsgm1fCDP5n135x29UA_nhc0YcnWVNuaVYleXuda-LWEBBN54wsd/pub?output=csv" 

def limpar_html(texto):
    if not isinstance(texto, str): return ""
    # Remove tags HTML e espaços extras
    clean = re.compile('<.*?>')
    texto_limpo = re.sub(clean, '', texto)
    return " ".join(texto_limpo.split())

def main():
    try:
        # Lê o CSV ignorando erros de linha para maior estabilidade
        df = pd.read_csv(URL_PLANILHA, on_bad_lines='skip')
        
        html = """<!DOCTYPE html>
<html lang="pt-br">
<head><meta charset="UTF-8"><title>Catalogo de Produtos</title></head>
<body>
<h1>CATÁLOGO DE PRODUTOS</h1>
"""
        
        for _, linha in df.iterrows():
            # Pegando os nomes exatos das colunas da sua planilha
            nome = linha.get('nome', 'Produto sem nome')
            preco = linha.get('preco-cheio', 'Consultar')
            marca = linha.get('marca', 'N/A')
            desc = limpar_html(str(linha.get('descricao-completa', '')))

            # Organizando o conteúdo para a IA do GHL ler perfeitamente
            html += f"<article style='border:1px solid #ccc; padding:15px; margin-bottom:10px; font-family: sans-serif;'>"
            html += f"<h2>PRODUTO: {nome}</h2>"
            html += f"<p><strong>MARCA:</strong> {marca}</p>"
            html += f"<p><strong>PREÇO:</strong> R$ {preco}</p>"
            html += f"<p><strong>DESCRIÇÃO:</strong> {desc}</p>"
            html += "</article>\n"
            
        html += "</body></html>"
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Arquivo index.html gerado com sucesso!")

    except Exception as e:
        print(f"Erro ao processar: {e}")

if __name__ == "__main__":
    main()
