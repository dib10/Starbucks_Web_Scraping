import requests
import pandas as pd

# URL base do JSON nutricional
url_base_nutricional = 'https://www.starbucks.com/bff/ordering/'

# Função para extrair informações nutricionais de um produto
def extrair_info_nutricional(num_produto, form_code):
    url_json = f'{url_base_nutricional}{num_produto}/{form_code}'
    response = requests.get(url_json)
    if response.status_code == 200:
        produto_json = response.json()['products'][0]
        # Verificar a existência de campos antes de acessá-los
        if 'sizes' in produto_json and produto_json['sizes']:
            size_info = produto_json['sizes'][0]
            if 'nutrition' in size_info and size_info['nutrition']:
                nutrition_info = size_info['nutrition']
                info = {
                    'serving_size': nutrition_info.get('servingSize', {}).get('displayValue', 'N/A'),
                    'calories': nutrition_info.get('calories', {}).get('displayValue', 'N/A'),
                    'total_fat': nutrition_info.get('additionalFacts', [{}])[0].get('displayValue', 'N/A'),
                    'saturated_fat': nutrition_info.get('additionalFacts', [{}])[0].get('subfacts', [{}])[0].get('displayValue', 'N/A'),
                    'trans_fat': nutrition_info.get('additionalFacts', [{}])[0].get('subfacts', [{}])[1].get('displayValue', 'N/A'),
                    'cholesterol': nutrition_info.get('additionalFacts', [{}])[1].get('displayValue', 'N/A'),
                    'sodium': nutrition_info.get('additionalFacts', [{}])[2].get('displayValue', 'N/A'),
                    'total_carbohydrate': nutrition_info.get('additionalFacts', [{}])[3].get('displayValue', 'N/A'),
                    'dietary_fiber': nutrition_info.get('additionalFacts', [{}])[3].get('subfacts', [{}])[0].get('displayValue', 'N/A'),
                    'sugars': nutrition_info.get('additionalFacts', [{}])[3].get('subfacts', [{}])[1].get('displayValue', 'N/A'),
                    'protein': nutrition_info.get('additionalFacts', [{}])[4].get('displayValue', 'N/A'),
                    'caffeine': next((fact.get('displayValue', 'N/A') for fact in nutrition_info.get('additionalFacts', []) if fact.get('displayName') == 'Caffeine'), 'N/A')
                }
                return info
    return None

# Função para extrair informações do menu
def extrair_informacoes(menu, caminho=[]):
    ignorar_categoria = ['merchandise', 'at home coffee']
    resultados = []
    for item in menu:
        novo_caminho = caminho + [item['name'].lower()]  # Convertendo o nome para minúsculas para comparação
        if 'children' in item and item['children']:
            # Continua a busca se houver subcategorias
            resultados.extend(extrair_informacoes(item['children'], novo_caminho))
        if 'products' in item and item['products']:
            for produto in item['products']:
                # Verifica se qualquer parte do novo_caminho contém as categorias a serem ignoradas
                if any(categoria in novo_caminho for categoria in ignorar_categoria):
                    continue
                # Garantir que novo_caminho tenha exatamente 3 elementos
                while len(novo_caminho) < 3:
                    novo_caminho.append(None)
                categoria, subcategoria, subsubcategoria = novo_caminho[:3]
                if subsubcategoria is None:
                    subsubcategoria = subcategoria
                uri_produto = produto.get('uri')
                url_produto = url_base_menu + uri_produto  # aqui é a url direta para o produto
                num_produto = produto['productNumber']
                form_code = produto['formCode']
                produto_info = {
                    'Name': produto['name'],
                    'Category': categoria,
                    'Subcategory': subcategoria,
                    'Subsubcategory': subsubcategoria,
                    'URL': url_produto
                }
                
                # Adiciona as informações nutricionais ao produto_info
                info_nutricional = extrair_info_nutricional(num_produto, form_code)
                if info_nutricional:
                    produto_info.update(info_nutricional) # aqui é o merge dos dois dicionários
                
                resultados.append(produto_info)
    return resultados

# URL base do menu
url_base_menu = 'https://www.starbucks.com/menu'

# Realizar a requisição HTTP e verificar se foi bem-sucedida
response = requests.get('https://www.starbucks.com/bff/ordering/menu')
if response.status_code == 200:
    data = response.json()  # Extrair os dados JSON da resposta
    
    # Extrair informações começando do nível mais alto
    resultados = extrair_informacoes(data['menus'])
    
    # Salvar os resultados em um arquivo CSV
    df = pd.DataFrame(resultados)
    df.to_csv('starbucks_menu.csv', index=False, encoding='utf-8-sig')
    
    print(f"Produtos encontrados: {len(resultados)}")
    print(f"{resultados[212]}")  # Exemplo de impressão de um produto específico
    
else:
    print(f"Erro ao acessar o JSON: Status code {response.status_code}")
