from config import *
sleep(2)

# Identificando o cardápio

from selenium.webdriver.common.action_chains import ActionChains

# Identificando o cardápio
nav_cardapio = navegador.find_element(By.CSS_SELECTOR, '.lgMax-hidden.py3.sideNav___sd5gv')

itens_cardapio = nav_cardapio.find_elements(By.CSS_SELECTOR, 'li.my3')

# Clicando em cada item do cardápio
for item in itens_cardapio:
    # Rola a página até o item
    navegador.execute_script("arguments[0].scrollIntoView();", item)

    # Rolar um pouco para cima
    navegador.execute_script("window.scrollBy(0, -100);")

    # Clique no item
    ActionChains(navegador).move_to_element(item).click(item).perform()

    sleep(1)
    print(navegador.current_url)



