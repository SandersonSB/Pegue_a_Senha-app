
# app.py
# Aplicativo web para visualizar o desempenho de times de futebol

# Importa as bibliotecas necessárias
import streamlit as st  # cria a interface do app
import pandas as pd  # manipula os dados
import seaborn as sns  # cria gráficos mais bonitos
import matplotlib.pyplot as plt  # biblioteca de gráficos

# Configura o visual da página do app
st.set_page_config(page_title="Análise de Resultados por Time", layout="wide")

abas = st.tabs(["📘 Introdução", "📊 Histórico de temporadas", "🔢 Probabilidade", "🤔 Curiosidades"])

# Aba 0: Introdução
with abas[0]:
    st.header("Introdução")
    st.whrite ("Intordução! EM DESENVOLVIMENTO 🛠️🔧.")

# Aba 1: Histórico de temporadas
with abas[1]:
    st.header("Analise de Temporada")
    st.title("📊 Análise de Resultados de Times de Futebol")

    # Função para carregar e preparar os dados, usando cache para não carregar toda hora
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

        newdf1 = df.groupby(['Country', 'League', 'Season', 'Home'])['Res'].value_counts().reset_index(name='count')
        newdf1['Res'] = newdf1['Res'].replace({
            'A': 'DERROTA/DENTRO DE CASA',
            'D': 'EMPATE/DENTRO DE CASA',
            'H': 'VITORIA/DENTRO DE CASA'
        })

        newdf2 = df.groupby(['Country', 'League', 'Season', 'Away'])['Res'].value_counts().reset_index(name='count')
        newdf2['Res'] = newdf2['Res'].replace({
            'A': 'VITORIA/FORA DE CASA',
            'D': 'EMPATE/FORA DE CASA',
            'H': 'DERROTA/FORA DE CASA'
        })

        manlydf = pd.concat([newdf1, newdf2], ignore_index=True)
        manlydf['Time_Referente'] = manlydf['Home'].combine_first(manlydf['Away'])
        manlydf['Season'] = manlydf['Season'].astype(int)

        return manlydf

    # Carrega os dados
    manlydf = load_data()

    # Cria a lista de times únicos disponíveis para escolher
    times_disponiveis = sorted(manlydf['Time_Referente'].dropna().unique())

    # Caixa de seleção para o usuário escolher um ou mais times
    times_selecionados = st.multiselect("Selecione os times para análise:", times_disponiveis)

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

# Aba 2: Probabilidades
with abas[2]:
    st.header("Probabilidades")
    st.whrite ("Probabilidades - EM DESENVOLVIMENTO! 🛠️🔧.")

# Aba 3: Curiosidades
with abas[3]:
    st.header("Curiosidades")
    st.whrite ("Curiosidades -  EM DESENVOLVIMENTO! 🛠️🔧.")
