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

# Botões para cada tipo de registro
if st.button("Button 1"):
    # Obter a hora atual
    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Criar nova linha com nome, botão e hora
    new_row = {"Name": name, "Button": "Button 1", "SubmissionDateTime": submission_datetime}

    # Adicionar nova linha aos dados existentes
    new_rows = existing_data_reservations.to_dict(orient="records")
    new_rows.append(new_row)

    # Atualizar a planilha com os novos dados
    conn.update(worksheet="Folha", data=new_rows)

    st.success("Details successfully submitted!")

if st.button("Button 2"):
    # Obter a hora atual
    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Criar nova linha com nome, botão e hora
    new_row = {"Name": name, "Button": "Button 2", "SubmissionDateTime": submission_datetime}

    # Adicionar nova linha aos dados existentes
    new_rows = existing_data_reservations.to_dict(orient="records")
    new_rows.append(new_row)

    # Atualizar a planilha com os novos dados
    conn.update(worksheet="Folha", data=new_rows)

    st.success("Details successfully submitted!")

if st.button("Button 3"):
    # Obter a hora atual
    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Criar nova linha com nome, botão e hora
    new_row = {"Name": name, "Button": "Button 3", "SubmissionDateTime": submission_datetime}

    # Adicionar nova linha aos dados existentes
    new_rows = existing_data_reservations.to_dict(orient="records")
    new_rows.append(new_row)

    # Atualizar a planilha com os novos dados
    conn.update(worksheet="Folha", data=new_rows)

    st.success("Details successfully submitted!")

if st.button("Button 4"):
    # Obter a hora atual
    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Criar nova linha com nome, botão e hora
    new_row = {"Name": name, "Button": "Button 4", "SubmissionDateTime": submission_datetime}

    # Adicionar nova linha aos dados existentes
    new_rows = existing_data_reservations.to_dict(orient="records")
    new_rows.append(new_row)

    # Atualizar a planilha com os novos dados
    conn.update(worksheet="Folha", data=new_rows)

    st.success("Details successfully submitted!")
