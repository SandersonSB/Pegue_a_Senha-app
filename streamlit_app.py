# app.py
# com chat

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração inicial
st.set_page_config(page_title="Análise de Resultados por Time", layout="wide")

# Título do app
st.title("📊 Análise de Resultados de Times de Futebol")

# Carregar os dados
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/SandersonSB/Pega-Senha-Project/main/BRA.csv'
    df = pd.read_csv(url)

    codigotimes = 3090
    teams = pd.concat([df['Home'], df['Away']]).unique()
    team_ids = {team: i for i, team in enumerate(teams)}
    df['Home Team ID'] = df['Home'].map(team_ids) + codigotimes
    df['Away Team ID'] = df['Away'].map(team_ids) + codigotimes
    df['Cod Match'] = df['Home Team ID'].astype(str) + "-" + df['Away Team ID'].astype(str)

    newdf1 = df.groupby(['Country','League','Season','Home'])['Res'].value_counts().reset_index()
    newdf1['Res'] = newdf1['Res'].replace({'A': 'DERROTA/DENTRO DE CASA', 'D': 'EMPATE/DENTRO DE CASA', 'H': 'VITORIA/DENTRO DE CASA'})

    newdf2 = df.groupby(['Country','League','Season','Away'])['Res'].value_counts().reset_index()
    newdf2['Res'] = newdf2['Res'].replace({'A': 'VITORIA/FORA DE CASA', 'D': 'EMPATE/FORA DE CASA', 'H': 'DERROTA/FORA DE CASA'})

    manlydf = pd.concat([newdf1, newdf2], ignore_index=True)
    manlydf['Time_Referente'] = manlydf['Home'].combine_first(manlydf['Away'])
    manlydf['Season'] = manlydf['Season'].astype(int)

    return manlydf

manlydf = load_data()

# Interface para seleção dos times
times_disponiveis = sorted(manlydf['Time_Referente'].dropna().unique())
times_selecionados = st.multiselect("Selecione os times para análise:", times_disponiveis)

# Mostrar gráfico se ao menos um time for selecionado
if times_selecionados:
    df_filtrado = manlydf[manlydf['Time_Referente'].isin(times_selecionados)]
    df_grouped = df_filtrado.groupby(['Season', 'Res'], as_index=False)['count'].sum()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_grouped, x='Season', y='count', hue='Res', marker='o')
    plt.xticks(sorted(manlydf['Season'].unique()))
    plt.title(f'Contagem de Resultados por Temporada\nTimes: {", ".join(times_selecionados)}')
    plt.xlabel('Temporada')
    plt.ylabel('Contagem de Resultados')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.info("👈 Por favor, selecione pelo menos um time na lista acima.")
