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
    button_pressed = None
    if st.button("Button 1"):
        button_pressed = "Button 1"
    elif st.button("Button 2"):
        button_pressed = "Button 2"
    elif st.button("Button 3"):
        button_pressed = "Button 3"
    elif st.button("Button 4"):
        button_pressed = "Button 4"

    # Submeter o formulário
    submit_button = st.form_submit_button(label="Submit Details")
    if submit_button:
        if button_pressed:
            # Obter o timestamp atual
            submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Criar nova linha com o nome do botão e o timestamp
            new_row = {
                "Name": button_pressed,
                "Timestamp": submission_datetime
            }
        else:
            # Criar nova linha com o nome inserido e o timestamp
            submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = {
                "Name": name,
                "Timestamp": submission_datetime
            }

        # Adicionar a nova linha aos dados existentes
        new_rows = existing_data_reservations.to_dict(orient="records")
        new_rows.append(new_row)

        # Atualizar a planilha com os novos dados
        conn.update(worksheet="Folha", data=new_rows)

        # Exibir mensagem de sucesso
        st.success("Details successfully submitted!")
