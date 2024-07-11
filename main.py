import requests
import pandas as pd

url_base_menu = 'https://www.starbucks.com/menu'
# Realizar a requisição HTTP e verificar se foi bem-sucedida
response = requests.get('https://www.starbucks.com/bff/ordering/menu')
if response.status_code == 200:
    data = response.json()  # Extrair os dados JSON da resposta
    url_base_menu = 'https://www.starbucks.com/menu'  # URL base para os produtos
    
    def extrair_informacoes(menu, caminho=[]):
        resultados = []
        for item in menu:
            novo_caminho = caminho + [item['name'].lower()]  # Convertendo o nome para minúsculas para comparação
            if 'children' in item and item['children']:
                # Continua a busca se houver subcategorias
                resultados.extend(extrair_informacoes(item['children'], novo_caminho))
            if 'products' in item and item['products']:
                for produto in item['products']:
                    # Verifica se qualquer parte do novo_caminho contém as categorias a serem ignoradas
                    if any(categoria in novo_caminho for categoria in ['merchandise', 'at home coffee']):
                        continue
                    # Garantir que novo_caminho tenha exatamente 3 elementos
                    while len(novo_caminho) < 3:
                        novo_caminho.append(None)
                    categoria, subcategoria, subsubcategoria = novo_caminho[:3]
                    if subsubcategoria is None:
                        subsubcategoria = subcategoria
                    uri_produto = produto.get('uri')
                    url_produto = url_base_menu + uri_produto #aqui é a url direta para o produto
                    num_produto = produto['productNumber']
                    form_code = produto['formCode']    
                    produto_info = {
                        'Nome': produto['name'],
                        'Categoria': categoria,
                        'Subcategoria': subcategoria,
                        'Subsubcategoria': subsubcategoria,
                        'URL': url_produto,
                        'ProductNumber': num_produto,
                        'FormCode': form_code,
                    }
                    resultados.append(produto_info)
        return resultados

    # Extrair informações começando do nível mais alto
    resultados = extrair_informacoes(data['menus'])
    # Salvar os resultados em um arquivo CSV
    df = pd.DataFrame(resultados)
    df.to_csv('starbucks_menu.csv', index=False, encoding='utf-8-sig')
    
    print(f"Produtos encontrados: {len(resultados)}")
    print(f"{resultados[213]}")  # Exemplo de impressão de um produto específico
    
else:
    print(f"Erro ao acessar o JSON: Status code {response.status_code}")
