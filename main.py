import requests
import pandas as pd

url_base_menu = 'https://www.starbucks.com/menu'
url_base_nutri = 'https://www.starbucks.com/bff/ordering/'

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
                    # Garantir que novo_caminho tenha exatamente 3 elementos
                    while len(novo_caminho) < 3:
                        novo_caminho.append(None)
                    categoria, subcategoria, subsubcategoria = novo_caminho
                    if subsubcategoria is None:
                        subsubcategoria = subcategoria
                    uri_produto = produto.get('uri', 'Sem URL')
                    url_produto = url_base_menu + uri_produto
                    num_produto = produto['productNumber']  # Extrai o número do produto
                    url_nutri_produto = f'{url_base_nutri}{num_produto}/single'
                    produto_info = {
                        'Categoria': categoria,
                        'Subcategoria': subcategoria,
                        'Subsubcategoria': subsubcategoria,
                        'Nome': produto['name'],
                        'URL': url_produto,  # URL do produto ajustada
                        'ProductNumber': num_produto,  # Número do produto
                        'URL nutricional': url_nutri_produto,
                    }
                    resultados.append(produto_info)
        return resultados

    # Extrair informações começando do nível mais alto
    resultados = extrair_informacoes(data['menus'])

    # Salvar os resultados em um arquivo CSV
    df = pd.DataFrame(resultados)
    df.to_csv('starbucks_menu.csv', index=False, encoding='utf-8-sig')
    
    print(f"Produtos encontrados: {len(resultados)}")
    print(f"{resultados[2]}")  # Exemplo de impressão de um produto específico
    
else:
    print(f"Erro ao acessar o JSON: Status code {response.status_code}")
