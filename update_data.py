import pandas as pd
import re
import os

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQu8BfHaCDnt0y0YZmLK0Ntdf9Jzsgm1fCDP5n135x29UA_nhc0YcnWVNuaVYleXuda-LWEBBN54wsd/pub?output=csv" 
PRODUTOS_POR_PAGINA = 20  # Ajustado para ficar bem abaixo das 750 palavras

def limpar_texto(texto):
    if not isinstance(texto, str): return ""
    clean = re.compile('<.*?>')
    texto = re.sub(clean, '', texto)
    return " ".join(texto.split())[:400] # Limita a 400 caracteres para garantir espaço

def salvar_html(nome_arquivo, produtos):
    html = "<html><head><meta charset='UTF-8'></head><body>"
    for p in produtos:
        html += f"<div>PRODUTO:{p['nome']}|PRECO:{p['preco']}|MARCA:{p['marca']}|DESC:{p['desc']}</div><br>\n"
    html += "</body></html>"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    try:
        df = pd.read_csv(URL_PLANILHA)
        lista_produtos = []
        
        for _, row in df.iterrows():
            lista_produtos.append({
                "nome": str(row.get('nome', '')),
                "preco": str(row.get('preco-cheio', '')),
                "marca": str(row.get('marca', '')),
                "desc": limpar_texto(str(row.get('descricao-completa', '')))
            })

        # Divide a lista em blocos de 20
        for i in range(0, len(lista_produtos), PRODUTOS_POR_PAGINA):
            chunk = lista_produtos[i:i + PRODUTOS_POR_PAGINA]
            numero_pagina = (i // PRODUTOS_POR_PAGINA) + 1
            nome_arquivo = f"produtos_parte_{numero_pagina}.html"
            salvar_html(nome_arquivo, chunk)
            print(f"Gerado: {nome_arquivo}")

        # Cria um index.html com links para todas as partes (ajuda o crawler)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write("<html><body><h1>Catalogo</h1>")
            for j in range(1, (len(lista_produtos) // PRODUTOS_POR_PAGINA) + 2):
                f.write(f"<a href='produtos_parte_{j}.html'>Parte {j}</a><br>")
            f.write("</body></html>")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
