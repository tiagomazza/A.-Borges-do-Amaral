import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados existentes da planilha
def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, ttl=5)
    return existing_data.dropna(how="all")

def fill_missing_data(data_frame):
    default_entry_morning = pd.Timestamp.now().replace(hour=9, minute=0, second=0)
    default_exit_morning = pd.Timestamp.now().replace(hour=12, minute=30, second=0)
    default_entry_afternoon = pd.Timestamp.now().replace(hour=14, minute=30, second=0)
    default_exit_afternoon = pd.Timestamp.now().replace(hour=18, minute=0, second=0)
    
    for index, row in data_frame.iterrows():
        if pd.isnull(row['Entrada Manhã']):
            data_frame.at[index, 'Entrada Manhã'] = default_entry_morning
        if pd.isnull(row['Saída Manhã']):
            data_frame.at[index, 'Saída Manhã'] = default_exit_morning
        if pd.isnull(row['Entrada Tarde']):
            data_frame.at[index, 'Entrada Tarde'] = default_entry_afternoon
        if pd.isnull(row['Saída Tarde']):
            data_frame.at[index, 'Saída Tarde'] = default_exit_afternoon

def save_to_new_sheet(df, sheet_name):
    # Criar uma nova aba com o nome especificado pelo usuário e salvar os dados nela
    if st.button("Salvar em nova aba"):
        if sheet_name:
            try:
                conn.create(worksheet=sheet_name)
                conn.update(worksheet=sheet_name, data=df)
                st.success(f"Dados salvos na nova aba '{sheet_name}' com sucesso.")
            except Exception as e:
                st.error(f"Erro ao criar a nova aba: {e}")
        else:
            st.warning("Por favor, digite um nome para a nova aba.")

# Carregar dados existentes
existing_data_reservations = load_existing_data("Folha")

pagina_selecionada = st.sidebar.radio("Acessos", ["Marcação de Ponto", "Consultas", "Admin"])

# Determinar qual página exibir com base na seleção do usuário
if pagina_selecionada == "Marcação de Ponto":

    # Adicionar campo de PIN
    pin_digitado = st.text_input("Digite o seu PIN:")

    # Verificar se o PIN foi digitado
    if pin_digitado:
        # Ler os dados da aba "Dados" para encontrar o nome correspondente ao PIN inserido
        dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
        
        # Verificar se o PIN está na lista de PINs válidos
        if int(float(pin_digitado)) in dados["Pin"].tolist():
            nome = dados.loc[dados["Pin"] == int(float(pin_digitado)), "Nome"].iloc[0]
            
            # Dar as boas-vindas utilizando o nome correspondente
            st.write(f"😀 Bem-vindo, {nome}!")

            # Adicionar espaço entre a mensagem de boas-vindas e os botões
            st.write("")

            # Botões para cada tipo de registro
            if st.button("☕ Entrada Manhã"):
                # Obter a hora atual
                submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Criar nova linha com nome, botão e hora
                new_row = {"Name": nome, "Button": "Entrada Manhã", "SubmissionDateTime": submission_datetime}

                # Adicionar nova linha aos dados existentes
                new_rows = existing_data_reservations.to_dict(orient="records")
                new_rows.append(new_row)

                # Atualizar a planilha com os novos dados
                conn.update(worksheet="Folha", data=new_rows)

                st.success("Dados registrados com sucesso!")

            if st.button("🌮 Saída Manhã"):
                # Obter a hora atual
                submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Criar nova linha com nome, botão e hora
                new_row = {"Name": nome, "Button": "Saída Manhã", "SubmissionDateTime": submission_datetime}

                # Adicionar nova linha aos dados existentes
                new_rows = existing_data_reservations.to_dict(orient="records")
                new_rows.append(new_row)

                # Atualizar a planilha com os novos dados
                conn.update(worksheet="Folha", data=new_rows)

                st.success("Dados registrados com sucesso!")

            if st.button("🌄 Entrada Tarde"):
                # Obter a hora atual
                submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Criar nova linha com nome, botão e hora
                new_row = {"Name": nome, "Button": "Entrada Tarde", "SubmissionDateTime": submission_datetime}

                # Adicionar nova linha aos dados existentes
                new_rows = existing_data_reservations.to_dict(orient="records")
                new_rows.append(new_row)

                # Atualizar a planilha com os novos dados
                conn.update(worksheet="Folha", data=new_rows)

                st.success("Dados registrados com sucesso!")

            if st.button("😴 Saída Tarde"):
                # Obter a hora atual
                submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Criar nova linha com nome, botão e hora
                new_row = {"Name": nome, "Button": "Saída Tarde", "SubmissionDateTime": submission_datetime}

                # Adicionar nova linha aos dados existentes
                new_rows = existing_data_reservations.to_dict(orient="records")
                new_rows.append(new_row)

                # Atualizar a planilha com os novos dados
                conn.update(worksheet="Folha", data=new_rows)

                st.success("Dados registrados com sucesso
