import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

st.title("Registro")

# Função para carregar os dados existentes da planilha
def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, ttl=5)
    return existing_data.dropna(how="all")

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Carregar dados existentes
existing_data_reservations = load_existing_data("Folha")

# Formulário para inserir o nome
with st.form(key="vendor_form"):
    name = st.text_input(label="Name")

    submit_button = st.form_submit_button(label="Submit Details")
    if submit_button:
        # Obter a hora atual
        submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Criar nova linha com nome e hora
        new_row = {"Name": name, "SubmissionDateTime": submission_datetime}

        # Adicionar nova linha aos dados existentes
        new_rows = existing_data_reservations.to_dict(orient="records")
        new_rows.append(new_row)

        # Atualizar a planilha com os novos dados
        conn.update(worksheet="Folha", data=new_rows)

        st.success("Details successfully submitted!")
