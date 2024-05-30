import streamlit as st
import pandas as pd
from PIL import Image
import sqlite3

# Lendo o caminho do banco de dados a partir dos segredos
db_path = st.secrets["database"]["path"]

def main():
    # Estabelecer conexão com o banco de dados SQLite
    conn = sqlite3.connect(db_path)

    # Ler os dados do banco de dados usando pandas
    df_yahoo_cotacao = pd.read_sql("SELECT * FROM cotacao_yahoo.db;", conn)

    # Fechar a conexão com o banco de dados
    conn.close()

    # Personalizar o título da página
    st.set_page_config(
        page_title="Cripto Currencies",
        page_icon="💸",
        layout="wide"
    )

    # Carregar a imagem da sua logo
    logo = Image.open('bitcoin2.png')  # Substitua 'caminho/para/sua/logo.png' pelo caminho correto para sua imagem

    st.title('CriptoMoedas Ao Vivo')
    st.write("# CRYPTO CURRENCIES💸")
    st.write("""
    Criptomoedas são moedas digitais ou virtuais que usam criptografia para segurança. 
    Elas operam de forma descentralizada na maioria das vezes, utilizando a tecnologia blockchain.
    A seguir, apresentamos algumas das principais criptomoedas com suas respectivas mudanças de preço e valor de mercado.
    """)

    st.header('Tabela de Dados Gerais')
    st.dataframe(df_yahoo_cotacao, width=1500, height=500, hide_index=True)

    # Exibir a logo
    st.image(logo, width=100)  # Defina a largura desejada para a logo

if __name__ == "__main__":
    main()
