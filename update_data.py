import requests
import pandas as pd
import re

# COLE O SEU LINK DO GOOGLE SHEETS (CSV) ABAIXO:
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vReYUwaAC9Qcpwe7zKR7aeP0MTMR7MWFF1G9_hvmR2kfDAealCE7wUoVUvMPCS1Zcl9yukdlfmLNODA/pub?output=csv"

def limpar_html(texto):
    if not isinstance(texto, str): return str(texto)
    return re.sub('<[^<]+?>', '', texto)

def main():
    df = pd.read_csv(URL_PLANILHA)
    html = "<html><head><meta charset='UTF-8'></head><body>"
    
    for _, linha in df.iterrows():
        # Ajuste o nome das colunas abaixo conforme sua planilha
        nome = linha.get('NOME', 'Produto')
        preco = linha.get('PREÇO', 'Consultar')
        desc = limpar_html(linha.get('DESCRIÇÃO', ''))
        
        html += f"<div>PRODUTO: {nome} | PREÇO: {preco} | INFO: {desc}</div><br>\n"
    
    html += "</body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
