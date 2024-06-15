import requests
import json

# request na api que retorna os dados do menu em json
url_json = 'https://www.starbucks.com/bff/ordering/menu'
response_json = requests.get(url_json)

if response_json.status_code == 200:
    dados = response_json.json()
    print("JSON carregado com sucesso")

    # Função para extrair os dados desejados
    lista_menu = []
    base_url_menu = 'https://www.starbucks.com/menu'

    def extrair_dados(dados, categoria=""):
        for item in dados:
            nome = item.get('name', 'N/A')
            if 'products' in item and item['products']:
                for produto in item['products']:
                    nome_produto = produto.get('name', 'N/A')
                    uri_produto = produto.get('uri', 'N/A')
                    lista_menu.append({
                        "Categoria": categoria,
                        "Subcategoria": nome,
                        "Produto": nome_produto,
                        "URL do Produto": base_url_menu + uri_produto
                    })
            if 'children' in item and item['children']:
                extrair_dados(item['children'], categoria=nome)

    # Iniciar a extração de dados
    if 'menus' in dados:
        extrair_dados(dados['menus'])
    
    # Salvando os dados em um arquivo
    with open('output.txt', 'w', encoding='utf-8') as f:
        for item in lista_menu:
            f.write(f"Categoria: {item['Categoria']}\n")
            f.write(f"Subcategoria: {item['Subcategoria']}\n")
            f.write(f"Produto: {item['Produto']}\n")
            f.write(f"URL do Produto: {item['URL do Produto']}\n")
            f.write("------------------------\n")
    
    print("Dados extraídos com sucesso")
    # print(lista_menu)
    print(f"Total de itens encontrados: {len(lista_menu)}")
else:
    print(f"Erro ao carregar JSON: {response_json.status_code}")
