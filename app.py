import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para escrever o número 1 na planilha do Google Sheets
def escrever_registro():
    # Obter a hora atual para registro na planilha
    hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Escrever o número e o timestamp na planilha
    existing_data = conn.read(worksheet="Folha", ttl=5)
    if existing_data is None:
        existing_data = pd.DataFrame(columns=["Nome", "Horário"])
    else:
        existing_data = pd.DataFrame(existing_data)
        
    existing_data = existing_data.append({"Nome": 1, "Horário": hora_atual}, ignore_index=True)
    conn.update(worksheet="Folha", data=existing_data.to_dict(orient="records"))

    st.success("Número e timestamp foram registrados na planilha!")

# Interface do Streamlit
st.title("Aplicativo para Registrar na Planilha")

# Botão para escrever o número 1 na planilha e registrar o timestamp
if st.button("Registrar na Planilha"):
    escrever_registro()
