import pandas as pd
import re

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQu8BfHaCDnt0y0YZmLK0Ntdf9Jzsgm1fCDP5n135x29UA_nhc0YcnWVNuaVYleXuda-LWEBBN54wsd/pub?output=csv" 

def limpar_html(texto):
    if not isinstance(texto, str): return ""
    # Remove tags HTML e códigos estranhos
    clean = re.compile('<.*?>')
    texto = re.sub(clean, '', texto)
    # Remove excesso de espaços e quebras de linha para diminuir o tamanho do arquivo
    return " ".join(texto.split())

def main():
    try:
        # Carrega apenas as colunas essenciais para economizar memória e tempo
        colunas_necessarias = ['nome', 'preco-cheio', 'marca', 'descricao-completa']
        df = pd.read_csv(URL_PLANILHA, usecols=lambda c: c in colunas_necessarias)
        
        # Se a planilha for gigantesca, vamos focar nos primeiros 400 produtos para evitar timeout
        # df = df.head(400) 

        html_content = "<html><head><meta charset='UTF-8'></head><body>"
        
        for _, row in df.iterrows():
            nome = str(row.get('nome', ''))
            preco = str(row.get('preco-cheio', ''))
            marca = str(row.get('marca', ''))
            desc = limpar_html(str(row.get('descricao-completa', '')))

            # Formato ultra-compacto: Nome | Preço | Marca | Descrição
            # Usamos apenas uma linha por produto para o arquivo carregar mais rápido
            html_content += f"<p>PRODUTO:{nome}|PRECO:{preco}|MARCA:{marca}|DESC:{desc}</p>\n"
            
        html_content += "</body></html>"
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Sucesso: Arquivo otimizado gerado.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
