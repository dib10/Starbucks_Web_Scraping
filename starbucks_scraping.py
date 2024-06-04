from config import *
sleep(5)

# Identificando o cardápio

nav_cardapio = navegador.find_element(By.CSS_SELECTOR, '.lgMax-hidden.py3.sideNav___sd5gv')

#debuggando o cardápio, printando o texto
texto_cardapio = nav_cardapio.text
print(texto_cardapio)