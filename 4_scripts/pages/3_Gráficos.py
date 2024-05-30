import sqlalchemy as sqa 
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Cripto Currencies",
    page_icon="💸",
    layout="wide")

#Criar a interface com o banco
engine = sqa.create_engine("sqlite:///df_yahoo.db", echo=True)
conn = engine.connect()

#Ler os dados e criar um dataframe
yahoo= pd.read_sql('cotacao_yahoo.db', con=conn)
yahoo_cotacao = pd.DataFrame(yahoo, columns=['name', 'price', 'change', 'per_market', 'market'])


yahoo = st.session_state["data"] = yahoo


st.title("Comparação de Criptomoedas")

if isinstance(yahoo, pd.DataFrame) and 'name' in yahoo.columns:
    # Selecionar criptomoeda para comparação
    selected_crypto = st.selectbox("Selecione a criptomoeda para comparar", yahoo['name'])

    # Verificar se a criptomoeda selecionada está no DataFrame
    if selected_crypto in yahoo['name'].values:
        # Encontrar os dados da criptomoeda selecionada
        selected_data = yahoo[yahoo['name'] == selected_crypto].iloc[0]

        # Exibir tabela de comparação
        st.subheader("Tabela de Comparação")

        #Ajustar tamanho do gráfico
        graph_width = 1000
        graph_height = 600

        # Adicionar coluna com status de comparação
        yahoo['selected_crypto'] = yahoo['name'] == selected_crypto
        yahoo_comparison = yahoo.copy()
        yahoo_comparison['status'] = yahoo_comparison.apply(
            lambda row: 'Selecionado' if row['selected_crypto'] else 'Comparação', axis=1)
        yahoo_comparison = yahoo_comparison.drop(columns=['selected_crypto'])

        # Estilizar a tabela
        def highlight_row(row):
            if row.status == 'Selecionado':
                return ['background-color: yellow'] * len(row)
            else:
                return [''] * len(row)

        st.dataframe(yahoo_comparison.style.apply(highlight_row, axis=1))

        # Exibir gráficos de comparação
        st.subheader("Gráficos de Comparação")

        # Preço
        fig_price = px.bar(yahoo, x='name', y='price', title='Comparação de Preço',
                           labels={'name': 'Criptomoeda', 'price': 'Preço'},
                           color='name', color_discrete_map={selected_crypto: 'blue'})
        st.plotly_chart(fig_price)

        # Mudança
        fig_change = px.bar(yahoo, x='name', y='change', title='Comparação de Mudança',
                            labels={'name': 'Criptomoeda', 'change': 'Mudança'},
                            color='name', color_discrete_map={selected_crypto: 'blue'})
        st.plotly_chart(fig_change)

        # Valor de Mercado
        fig_market = px.bar(yahoo, x='name', y='market', title='Comparação de Valor de Mercado',
                            labels={'name': 'Criptomoeda', 'market': 'Valor de Mercado'},
                            color='name', color_discrete_map={selected_crypto: 'blue'})
        st.plotly_chart(fig_market)
   
