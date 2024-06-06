import requests
import json
from bs4 import BeautifulSoup

#request para a pagina
response = requests.get('https://www.starbucks.com/menu')

# Parseando o HTML
soup = BeautifulSoup(response.text, 'html.parser')

#abrindo o arquivo json
with open('menu.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    base_url = 'https://www.starbucks.com/menu/'

# a partir do arquivo json, vamos pegar o nome e a url de cada menu
#links para cada menu

dict_menu = {}

# Irei armazenar as urls do cardápio em um dicionário, com base no JSON eu extraí o nome base das categorias e complemento a url com o nome da categoria e do subcategoria por exemplo: https://www.starbucks.com/menu/drinks/hot-coffees , hot-coffees é subcategoria do menu drinks.

#nesse caso, 
for menu in  data['menus']:
    menu_name = menu['name']
    if 'children' in menu:
        for child in menu['children']:
            child_name = child['name']
            child_url = base_url + menu_name.replace(' ', '-').lower() + '/' + child_name.replace(' ', '-').lower()
            dict_menu[child_name] = child_url
            print("Menu:", child_name)
            print("URL:", child_url)

print(dict_menu)