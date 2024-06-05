import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

#configurando o webdriver
navegador = webdriver.Chrome()
navegador.get('https://www.starbucks.com/menu/drinks/hot-coffees')

#request para a pagina
response = requests.get('https://www.starbucks.com')
# resposta_codigo = response.status_code
# print(resposta_codigo)