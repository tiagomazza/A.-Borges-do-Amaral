import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

st.title("Registro")

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados existentes da planilha
def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, usecols=list(range(11)), ttl=5)
    return existing_data.dropna(how="all")

# Carregar os dados existentes
existing_data_reservations = load_existing_data("Folha")

with st.form(key="vendor_form"):
    # Adicionar campo para o nome
    name = st.text_input(label="Name")

    # Adicionar 4 botões adicionais
    button1_clicked = st.form_submit_button(label="Button 1")
    button2_clicked = st.form_submit_button(label="Button 2")
    button3_clicked = st.form_submit_button(label="Button 3")
    button4_clicked = st.form_submit_button(label="Button 4")

    # Obter o nome do botão clicado
    if button1_clicked:
        button_name = "Button 1"
    elif button2_clicked:
        button_name = "Button 2"
    elif button3_clicked:
        button_name = "Button 3"
    elif button4_clicked:
        button_name = "Button 4"
    else:
        button_name = None

    # Submeter o formulário
    if st.form_submit_button(label="Submit Details"):
        # Verificar se algum botão foi clicado
        if button_name:
            # Obter o timestamp atual
            submission_datetime = datetime.now().strft
