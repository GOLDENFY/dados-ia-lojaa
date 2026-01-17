import pandas as pd
import re

# Coloque aqui o seu link CSV do Google Sheets
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQu8BfHaCDnt0y0YZmLK0Ntdf9Jzsgm1fCDP5n135x29UA_nhc0YcnWVNuaVYleXuda-LWEBBN54wsd/pub?output=csv" 

def limpar_html(texto):
    if not isinstance(texto, str): return ""
    # Remove tags HTML para a IA ler apenas o texto limpo
    clean = re.compile('<.*?>')
    return re.sub(clean, '', texto).strip()

def main():
    try:
        # Lê a planilha usando os nomes das colunas
        df = pd.read_csv(URL_PLANILHA)
        
        html_content = """<!DOCTYPE html>
<html lang="pt-br">
<head><meta charset="UTF-8"><title>Catalogo</title></head>
<body>
<h1>Catálogo de Produtos</h1>
"""
        
        for _, row in df.iterrows():
            # Mapeamento baseado na sua planilha real
            nome = str(row.get('nome', 'Produto sem nome'))
            preco = str(row.get('preco-cheio', 'Consultar'))
            marca = str(row.get('marca', 'N/A'))
            # Limpa o HTML da descrição (como os <h3> e <span> que vimos na Torre de Tomada)
            descricao = limpar_html(str(row.get('descricao-completa', '')))

            # Cria um bloco de texto que o GoHighLevel entende facilmente
            html_content += f"<div style='border:1px solid #000; margin:10px; padding:10px;'>"
            html_content += f"<h2>PRODUTO: {nome}</h2>"
            html_content += f"<p><strong>PREÇO:</strong> R$ {preco}</p>"
            html_content += f"<p><strong>MARCA:</strong> {marca}</p>"
            html_content += f"<p><strong>DESCRIÇÃO:</strong> {descricao}</p>"
            html_content += "</div>\n"
            
        html_content += "</body></html>"
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Arquivo index.html gerado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
