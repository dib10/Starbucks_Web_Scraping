import json
import requests
import pandas as pd

# Realizar a requisição HTTP e verificar se foi bem-sucedida
response = requests.get('https://www.starbucks.com/bff/ordering/menu')
if response.status_code == 200:
    data = response.json()  # Extrair os dados JSON da resposta
    url_base_menu = 'https://www.starbucks.com/menu'  # URL base para os produtos
    
    def extrair_informacoes(menu, caminho=[]):
        resultados = []
        for item in menu:
            novo_caminho = caminho + [item['name']]
            if 'children' in item and item['children']:
                # Continua a busca se houver subcategorias
                resultados.extend(extrair_informacoes(item['children'], novo_caminho))
            if 'products' in item and item['products']:
                for produto in item['products']:
                    if 'merchandise' in novo_caminho[0].lower():
                        continue
                    # Para cada produto, extrai as informações necessárias
                    categoria, subcategoria, subsubcategoria = (novo_caminho + [None, None])[:3]
                    # Se subsubcategoria for None, recebe o valor de subcategoria
                    if subsubcategoria is None:
                        subsubcategoria = subcategoria
                    uri_produto = produto.get('uri', 'Sem URL')
                    url_produto = url_base_menu + uri_produto
                    produto_info = {
                        'Categoria': categoria,
                        'Subcategoria': subcategoria,
                        'Subsubcategoria': subsubcategoria,
                        'Nome': produto['name'],
                        'URL': url_produto,  # URL do produto ajustada
                        'URL nutricional': url_produto + '/nutrition'  # Corrigir o nome da coluna
                    }
                    resultados.append(produto_info)
        return resultados

    # Extrair informações começando do nível mais alto
    resultados = extrair_informacoes(data['menus'])

else:
    print(f"Erro ao acessar o JSON: Status code {response.status_code}")
print(f"Produtos encontrados: {len(resultados)}")

print(f"{resultados[251]}")

# DATAFRAME
df = pd.DataFrame(resultados)
df.to_csv('starbucks_menu.csv', index=False, encoding='utf-8-sig')
# print(df.head())

