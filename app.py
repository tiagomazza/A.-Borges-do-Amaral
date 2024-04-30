import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para escrever o número 1 na planilha do Google Sheets
def escrever_numero():
    # Definir o número a ser escrito
    numero = 1
    
    # Obter a hora atual para registro na planilha
    hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Escrever o número na planilha
    conn.update(
        worksheet="Nome_da_sua_planilha",  # Substituir pelo nome da sua planilha
        data=[{"Número": numero, "Timestamp": hora_atual}]
    )

    st.success("Número 1 foi escrito na planilha!")

# Interface do Streamlit
st.title("Aplicativo para Escrever na Planilha")

# Botão para escrever o número 1 na planilha quando clicado
if st.button("Escrever Número 1 na Planilha"):
    escrever_numero()
