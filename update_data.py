import requests
import pandas as pd
import re

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQu8BfHaCDnt0y0YZmLK0Ntdf9Jzsgm1fCDP5n135x29UA_nhc0YcnWVNuaVYleXuda-LWEBBN54wsd/pub?output=csv" # Mantenha o seu link real aqui

def limpar_html(texto):
    if not isinstance(texto, str): return str(texto)
    return re.sub('<[^<]+?>', '', texto)

def main():
    df = pd.read_csv(URL_PLANILHA)
    
    # Criando um HTML mais "profissional" para o crawler não dar erro
    html = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Base de Conhecimento Produtos</title>
</head>
<body>
    <h1>Catálogo de Produtos</h1>
"""
    
    for _, linha in df.iterrows():
        nome = linha.iloc[0] 
        preco = linha.iloc[1]
        desc = limpar_html(linha.iloc[2])
        
        html += f"<article style='margin-bottom:20px; border-bottom:1px solid #eee;'>"
        html += f"<h2>{nome}</h2>"
        html += f"<p><strong>Preço:</strong> {preco}</p>"
        html += f"<p><strong>Descrição:</strong> {desc}</p>"
        html += "</article>\n"
    
    html += "</body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
