import requests
from bs4 import BeautifulSoup

#request para a pagina
response_html = requests.get('https://www.starbucks.com/menu')

# Parseando o HTML
soup = BeautifulSoup(response_html.text, 'html.parser')

base_url = 'https://www.starbucks.com/menu'
url_json = 'https://www.starbucks.com/bff/ordering/menu'
response_json = requests.get(url_json)

if response_json.status_code == 200:
    data = response_json.json()
    print("JSON carregado com sucesso")
# a partir do arquivo json, vamos pegar o nome e a url de cada menu


dict_menu = {}

# Irei armazenar as urls do cardápio em um dicionário, com base no JSON eu extraí o nome base das categorias e complemento a url com o nome da categoria e da subcategoria por exemplo: https://www.starbucks.com/menu/drinks/hot-coffees , hot-coffees é subcategoria do menu drinks.
dict_menu = {}

for menu in  data['menus']:
    if 'children' in menu:
        for child in menu['children']:
            child_name = child['name']
            child_url = base_url + child['uri']
            dict_menu[child_name] = child_url
            print("Categoria:", child_name)
            print("URL:", child_url)

print(dict_menu)

#aqui vamos pegar a url nutricional de cada produto, por exxemplo ela é composta por https://www.starbucks.com/menu/product/406/hot, é a uri

dict_product = {}
# Pegar a URI de cada produto
dict_product = {}
for menu in  data['menus']:
    base_url_product = 'https://www.starbucks.com/menu'
    if 'children' in menu:
        for child in menu['children']:
            if 'children' in child:
                for subchild in child['children']:
                    subcategory_name = subchild['name']
                    subcategory_url = base_url + subchild['uri']
                    print("\nSubcategoria:", subcategory_name)
                    print("URL:", subcategory_url)
                    if 'products' in subchild:
                        for product in subchild['products']:
                            product_name = product['name']
                            product_uri = product['uri']
                            dict_product[product_name] = base_url_product + product_uri
                            print("\nProduto:", product_name)
                            print("URL do Produto:", base_url_product + product_uri)

print(dict_product)