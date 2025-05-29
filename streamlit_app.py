# app.py
# Aplicativo web criado com Streamlit para visualizar o desempenho de times de futebol

# 📚 Importando as bibliotecas necessárias para o app funcionar
import streamlit as st  # Cria a interface visual do aplicativo
import pandas as pd  # Trabalha com os dados em forma de tabela
import seaborn as sns  # Faz gráficos mais bonitos
import matplotlib.pyplot as plt  # Mostra os gráficos na tela
import time  # Usado para pausar por alguns segundos (efeitos visuais)

# 🔧 CONFIGURAÇÃO INICIAL DO APLICATIVO - Isso sempre deve ser a primeira coisa depois dos imports
st.set_page_config(
    page_title="Pegue a Senha",  # Título que aparece na aba do navegador
    layout="wide"  # Define o layout como mais espaçado (melhor para gráficos)
)

# 🟣 TÍTULO PRINCIPAL DO APP COM ESTILO PERSONALIZADO
st.markdown(
    "<h1 style='text-align: center; color: #6c63ff;'>Pegue a Senha 🎲</h1>",
    unsafe_allow_html=True
)

# 🖼️ UPLOAD DO LOGOTIPO (caso o usuário queira carregar uma imagem da empresa)
logo = st.file_uploader("Envie aqui o logotipo da empresa (formatos aceitos: png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

# Verifica se o usuário enviou um arquivo de imagem
if logo:
    st.image(logo, width=200)  # Mostra o logo com largura de 200 pixels

    # Mensagem de boas-vindas
    st.markdown(
        "<h2 style='text-align: center; color: #4CAF50;'>Seja Bem-vindo ao Pegue a Senha 🎰</h2>",
        unsafe_allow_html=True
    )

    # Animação de carregamento por 2 segundos
    with st.spinner("Iniciando o sistema..."):
        time.sleep(2)  # Espera 2 segundos para criar um efeito

        st.balloons()  # Solta balões na tela

    st.divider()  # Linha para separar o topo do restante do conteúdo

# 🧭 CRIA AS ABAS DO APP
abas = st.tabs([
    "📘 Introdução", 
    "📊 Histórico de temporadas", 
    "🔢 Probabilidade", 
    "🤔 Curiosidades"
])

# ➤ ABA 1: INTRODUÇÃO
with abas[0]:
    st.header("Introdução")
    st.write("Introdução! EM DESENVOLVIMENTO 🛠️🔧.")

# ➤ ABA 2: HISTÓRICO DE TEMPORADAS
with abas[1]:
    st.header("Análise de Temporada")
    st.title("📊 Análise de Resultados de Times de Futebol")

    # Função que carrega os dados da internet e organiza tudo
    @st.cache_data
    def load_data():
        # Lê os dados direto do GitHub
        url = 'https://raw.githubusercontent.com/SandersonSB/Pega-Senha-Project/main/BRA.csv'
        df = pd.read_csv(url)

        # Cria códigos únicos para cada time
        codigotimes = 3090
        teams = pd.concat([df['Home'], df['Away']]).unique()
        team_ids = {team: i for i, team in enumerate(teams)}
        df['Home Team ID'] = df['Home'].map(team_ids) + codigotimes
        df['Away Team ID'] = df['Away'].map(team_ids) + codigotimes
        df['Cod Match'] = df['Home Team ID'].astype(str) + "-" + df['Away Team ID'].astype(str)

        # Agrupa os resultados dos jogos em casa
        newdf1 = df.groupby(['Country', 'League', 'Season', 'Home'])['Res'].value_counts().reset_index(name='count')
        newdf1['Res'] = newdf1['Res'].replace({
            'A': 'DERROTA/DENTRO DE CASA',
            'D': 'EMPATE/DENTRO DE CASA',
            'H': 'VITORIA/DENTRO DE CASA'
        })

        # Agrupa os resultados dos jogos fora de casa
        newdf2 = df.groupby(['Country', 'League', 'Season', 'Away'])['Res'].value_counts().reset_index(name='count')
        newdf2['Res'] = newdf2['Res'].replace({
            'A': 'VITORIA/FORA DE CASA',
            'D': 'EMPATE/FORA DE CASA',
            'H': 'DERROTA/FORA DE CASA'
        })

        # Junta os dois resultados (em casa e fora)
        manlydf = pd.concat([newdf1, newdf2], ignore_index=True)
        manlydf['Time_Referente'] = manlydf['Home'].combine_first(manlydf['Away'])  # Nome do time
        manlydf['Season'] = manlydf['Season'].astype(int)  # Garante que a temporada seja número

        return manlydf

    # Carrega os dados com a função acima
    manlydf = load_data()

    # Mostra os times disponíveis para escolher
    times_disponiveis = sorted(manlydf['Time_Referente'].dropna().unique())

    # Caixa onde o usuário escolhe um ou mais times
    times_selecionados = st.multiselect("Selecione os times para análise:", times_disponiveis)

    # Só mostra os gráficos se o usuário selecionar pelo menos 1 time
    if times_selecionados:
        # Filtra os dados pelos times escolhidos
        df_filtrado = manlydf[manlydf['Time_Referente'].isin(times_selecionados)]

        # Agrupa os resultados por temporada
        df_grouped = df_filtrado.groupby(['Season', 'Res'], as_index=False)['count'].sum()

        # Cria o gráfico de linha
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_grouped, x='Season', y='count', hue='Res', marker='o')
        plt.xticks(sorted(manlydf['Season'].unique()))
        plt.title(f'Contagem de Resultados por Temporada\nTimes: {", ".join(times_selecionados)}')
        plt.xlabel('Temporada')
        plt.ylabel('Contagem de Resultados')
        plt.grid(True)
        plt.tight_layout()

        # Mostra o gráfico no app
        st.pyplot(plt)
    else:
        st.info("👈 Por favor, selecione pelo menos um time na lista acima.")

# ➤ ABA 3: PROBABILIDADES
with abas[2]:
    st.header("Probabilidades")
    st.write("Probabilidades - EM DESENVOLVIMENTO! 🛠️🔧.")

# ➤ ABA 4: CURIOSIDADES
with abas[3]:
    st.header("Curiosidades")
    st.write("Curiosidades - EM DESENVOLVIMENTO! 🛠️🔧.")
