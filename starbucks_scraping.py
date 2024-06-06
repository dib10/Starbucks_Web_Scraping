import requests
import json
from bs4 import BeautifulSoup

#request para a pagina
response = requests.get('https://www.starbucks.com/menu')

# Parseando o HTML
soup = BeautifulSoup(response.text, 'html.parser')

with open('menu.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Iterar sobre os menus
for menu in data['menus']:
    print("Categoria:", menu['name'])
    
    # Se houver subcategorias, iterar sobre elas
    if 'children' in menu:
        for child in menu['children']:
            print("- Subcategoria:", child['name'])

            # Se houver produtos na subcategoria, iterar sobre eles
            if 'products' in child:
                for product in child['products']:
                    print("-- Produto:", product['name'])

            # Se houver sub-subcategorias, iterar sobre elas
            if 'children' in child:
                for subchild in child['children']:
                    print("-- Sub-subcategoria:", subchild['name'])

                    # Se houver produtos na sub-subcategoria, iterar sobre eles
                    if 'products' in subchild:
                        for product in subchild['products']:
                            print("--- Produto:", product['name'])