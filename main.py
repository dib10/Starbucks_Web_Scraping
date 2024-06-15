import requests

# Função para extrair os dados desejados
lista_menu = []
base_url_menu = 'https://www.starbucks.com/menu'

def extrair_menu_json(dados, categoria="", subcategoria=""):
    for item in dados:
        nome = item.get('name', 'N/A')

        if 'products' in item and item['products']:
            for produto in item['products']:
                nome_produto = produto.get('name', 'N/A')
                uri_produto = produto.get('uri', 'N/A')
                lista_menu.append({
                    "Categoria": categoria,
                    "Subcategoria": subcategoria,
                    "Sub-subcategoria": nome,
                    "Produto": nome_produto,
                    "URL do Produto": base_url_menu + uri_produto
                })

        if 'children' in item and item['children']:
            subcategoria_atual = subcategoria

            if 'name' in item and categoria == "":
                categoria = item['name']
            elif 'name' in item and subcategoria == "":
                subcategoria = item['name']

            extrair_menu_json(item['children'], categoria=categoria, subcategoria=subcategoria)

            # Reiniciar a subcategoria após cada iteração para manter a estrutura correta
            subcategoria = subcategoria_atual

# Request na API que retorna os dados do menu em JSON
url_json = 'https://www.starbucks.com/bff/ordering/menu'
resposta_json = requests.get(url_json)

# Verificando se a resposta foi bem sucedida

if resposta_json.status_code == 200:
    dados = resposta_json.json()['menus']
    print("JSON carregado com sucesso")

    #chamando a função que extrai os dados
    extrair_menu_json(dados)

    # Salvando os dados em um arquivo txt
    with open('output.txt', 'w', encoding='utf-8') as f:
        for item in lista_menu:
            f.write(f"Categoria: {item['Categoria']}\n")
            f.write(f"Subcategoria: {item['Subcategoria']}\n")
            f.write(f"Sub-subcategoria: {item['Sub-subcategoria']}\n")
            f.write(f"Produto: {item['Produto']}\n")
            f.write(f"URL do Produto: {item['URL do Produto']}\n")
            f.write("------------------------\n")

    print("Dados extraídos com sucesso")
    print(f"Total de itens encontrados: {len(lista_menu)}")
    print(lista_menu[0])
else:
    print(f"Erro ao carregar JSON: {resposta_json.status_code}")
