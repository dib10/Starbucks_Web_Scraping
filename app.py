import streamlit as st
import pandas as pd
import plotly.express as px

# Função para remover unidades e converter para float
def remover_unidades_e_converter(column, unit):
    return column.str.replace(f'[^0-9.]', '', regex=True).astype(float)

# Carregar a planilha de dados
df = pd.read_csv('starbucks_menu.csv')

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

st.title('Starbucks Menu')

st.dataframe(df)
