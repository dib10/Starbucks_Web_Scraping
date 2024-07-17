import streamlit as st
import pandas as pd
import plotly.express as px

# Função para remover unidades e converter para float
def remover_unidades_e_converter(column, unit):
    return column.str.replace(f'[^0-9.]', '', regex=True).astype(float)

# Carregar a planilha de dados
df = pd.read_csv('starbucks_menu.csv')
st.image('starbucks.png', width=100)
st.markdown("""
<p style='font-size: 20px;'>
    Powered by coffee and code. 
    If you liked my work, consider <a href='https://buymeacoffee.com/dib10'>buying me a coffee</a> ☕
</p>
<p style='font-size: 12px; color: gray;'>
    This site is not affiliated with Starbucks. It is a site with nutritional data extracted from the official Starbucks website at starbucks.com.
</p>
<hr>
""", unsafe_allow_html=True)

st.title('Starbucks Menu ☕️💚 ')

#exibir o dataframe
st.write(df)

# Remover unidades e converter colunas para numérico
df['serving_size'] = df['serving_size'].str.replace('[^0-9.]', '', regex=True).astype(float)
df['total_fat'] = remover_unidades_e_converter(df['total_fat'], 'g')
df['saturated_fat'] = remover_unidades_e_converter(df['saturated_fat'], 'g')
df['trans_fat'] = remover_unidades_e_converter(df['trans_fat'], 'g')
df['cholesterol'] = remover_unidades_e_converter(df['cholesterol'], 'mg')
df['sodium'] = remover_unidades_e_converter(df['sodium'], 'mg')
df['total_carbohydrate'] = remover_unidades_e_converter(df['total_carbohydrate'], 'g')
df['dietary_fiber'] = remover_unidades_e_converter(df['dietary_fiber'], 'g')
df['sugars'] = remover_unidades_e_converter(df['sugars'], 'g')
df['protein'] = remover_unidades_e_converter(df['protein'], 'g')
df['caffeine'] = remover_unidades_e_converter(df['caffeine'], 'mg')

# Filtrar linhas com valores não nulos nas colunas especificadas
df_clean = df.dropna(subset=['serving_size', 'calories', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol',
                             'sodium', 'total_carbohydrate', 'dietary_fiber', 'sugars', 'protein', 'caffeine'])


# Seletor para escolher a subcategoria
subcategoria = st.selectbox(
    'Choose the subcategory:',
    ('iced energy', 'hot coffees', 'cold coffees', 'starbucks refreshers® beverages', 'frappuccino® blended beverages', 'iced tea and lemonade', 'hot teas', 'milk, juice & more', 'hot breakfast', 'oatmeal & yogurt', 'bakery', 'lunch', 'snacks & sweets')
)

# Seletor para escolher o critério de filtragem
criterio = st.selectbox(
    'Choose the criteria to filter the highest item in:',
    ('calories', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium', 'total_carbohydrate', 'dietary_fiber', 'sugars', 'protein', 'caffeine')
)

# Mapeamento de unidades para cada critério
unidades = {
    'calories': 'kcal',
    'total_fat': 'g',
    'saturated_fat': 'g',
    'trans_fat': 'g',
    'cholesterol': 'mg',
    'sodium': 'mg',
    'total_carbohydrate': 'g',
    'dietary_fiber': 'g',
    'sugars': 'g',
    'protein': 'g',
    'caffeine': 'mg'
}

# Filtrar os itens da subcategoria escolhida
filtered_df = df_clean[df_clean['Subcategory'] == subcategoria]

# Encontrar o item com o valor máximo no critério selecionado
max_value = filtered_df[criterio].max()
min_value = filtered_df[criterio].min()

#checando se o valor máximo é 0, caso seja, exibe um gráfico de linha
if max_value == 0:
    st.write(f"The items in the category '{subcategoria}' do not have '{criterio.replace('_', ' ')}'.")
    # nesse caso, exibe gráfico de linha
    fig_line = px.line(filtered_df, x='Name', y=criterio, title=f'{subcategoria.title()} - {criterio.replace("_", " ").title()} ({unidades[criterio]})')
    fig_line.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_line)
else:
    most_value_item = filtered_df[filtered_df[criterio] == max_value]
    least_value_item = filtered_df[filtered_df[criterio] == min_value]
    
    # Mostrar o item com o valor máximo no critério selecionado
    st.write(f"📈 The item(s) with the highest {criterio.replace('_', ' ')} content in the subcategory '{subcategoria}' is/are:")
    st.write(most_value_item)

    st.write(f"📉 The item(s) with the lowest {criterio.replace('_', ' ')} content in the subcategory '{subcategoria}' is/are:")
    st.write(least_value_item)


    
    # gráfico de barras com os itens da subcategoria escolhida
    fig = px.bar(filtered_df, x='Name', y=criterio, title=f'{subcategoria.title()} - {criterio.replace("_", " ").title()} ({unidades[criterio]})',
                 color=criterio, color_continuous_scale=["#FFFFFF", "#036635"])
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig)


st.markdown("<hr>", unsafe_allow_html=True)
st.write('- 2,000 calories a day is used for general nutrition advice, but calorie needs vary.')
st.write('- Caffeine is an approximate value.')
st.write('- Nutrition information is calculated based on our standard recipes. Because our products may be customized, exact information may vary.')
st.write("- Items without nutritional information or with missing data were not included in the chart, but were included in the spreadsheet.")
st.write("- Items from the 'Bottled Beverages' subcategory were not included in the spreadsheet.")
st.write('- The beverage sizes selected to collect nutritional information were based on the smallest size offered for customization. Please note that there are various beverage sizes available. For more detailed information, refer to the *serving_size field in the spreadsheet above.')