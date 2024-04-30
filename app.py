import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def escrever_numero():
    sheet.update_cell(1, 1, '1')
    st.write("Número 1 foi escrito na planilha!")
    st.success("Número 1 foi escrito na planilha!")

# Interface do Streamlit
st.title("Aplicativo para Escrever na Planilha")

# Adicionar campo de PIN
pin_digitado = st.text_input("Digite o seu PIN:", type="password")

# Verificar se o PIN foi digitado
if pin_digitado:
    # Ler os dados da aba "Dados" para encontrar o nome correspondente ao PIN inserido
    dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
    
    # Verificar se o PIN está na lista de PINs válidos
    if int(float(pin_digitado)) in dados["Pin"].tolist():
        # Dar as boas-vindas utilizando o nome correspondente
        nome = dados.loc[dados["Pin"] == int(float(pin_digitado)), "Nome"].iloc[0]
        st.write(f"Bem-vindo, {nome}!")
        
        # Botão para escrever o número 1 na planilha quando clicado
        if st.button("Registrar Número 1 na Planilha"):
            escrever_numero()
    else:
        st.warning("PIN incorreto. Por favor, digite um PIN válido.")
