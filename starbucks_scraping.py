import requests
from bs4 import BeautifulSoup

# Fazendo a requisição para a página
response_html = requests.get('https://www.starbucks.com/menu')

# Parseando o HTML (embora neste caso específico não estejamos utilizando o soup)
soup = BeautifulSoup(response_html.text, 'html.parser')

base_url_menu = 'https://www.starbucks.com/menu' #para complementar a URL dos produtos extraídos
url_json = 'https://www.starbucks.com/bff/ordering/menu'
response_json = requests.get(url_json)

if response_json.status_code == 200:
    data = response_json.json()
    print("JSON carregado com sucesso")

    # Função para extrair os dados desejados
    lista_menu = []
    def extract_data(data):
        with open('output.txt', 'w', encoding='utf-8') as f:
            for menu in data.get('menus', []):
                menu_name = menu.get('name', 'N/A')
                for categoria in menu.get('children', []):
                    nome_categoria = categoria.get('name', 'N/A')
                    for sub_categoria in categoria.get('children', []):
                        sub_nome_categoria = sub_categoria.get('name', 'N/A')
                        for produto in sub_categoria.get('products', []):  # Corrigido aqui
                            nome_produto = produto.get('name', 'N/A')
                            uri_produto = produto.get('uri', 'N/A')
                            f.write(f"Categoria: {menu_name}\n")
                            f.write(f"Subcategoria: {nome_categoria}\n")
                            f.write(f"Sub-subcategoria: {sub_nome_categoria}\n")
                            f.write(f"Produto: {nome_produto}\n")
                            f.write(f"URL do Produto: {base_url_menu + uri_produto}\n")
                            lista_menu.append({
                                "Categoria": menu_name,
                                "Subcategoria": nome_categoria,
                                "Sub-subcategoria": sub_nome_categoria,
                                "Produto": nome_produto,
                                "URL do Produto": base_url_menu + uri_produto
                            })
                            f.write("------------------------\n")

    extract_data(data)
    print("Dados extraídos com sucesso")
    print(lista_menu)
    print(f"Total de itens encontrados: {len(lista_menu)}")
else:
    print(f"Erro ao carregar JSON: {response_json.status_code}")