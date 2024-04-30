import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados existentes da planilha
def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, ttl=5)
    return existing_data.dropna(how="all")

# Carregar dados existentes
existing_data_reservations = load_existing_data("Folha")

# Página de login
def login_page():
    st.title("Login")
    pin = st.text_input("Digite o seu PIN:", type="password")
    if pin:
        if authenticate_pin(pin):
            nome = authenticate_pin(pin)
            st.success(f"Bem-vindo, {nome}!")
            return "buttons_page"
        else:
            st.warning("PIN incorreto. Por favor, digite um PIN válido.")
    return None

# Página com botões
def buttons_page():
    st.title("Botões")
    if st.button("☕ Entrada Manhã"):
        register_button_click("Entrada Manhã")
    if st.button("🌮 Saída Manhã"):
        register_button_click("Saída Manhã")
    if st.button("🌄 Entrada Tarde"):
        register_button_click("Entrada Tarde")
    if st.button("😴 Saída Tarde"):
        register_button_click("Saída Tarde")

# Função para registrar o clique em um botão na planilha
def register_button_click(button_name):
    # Obter o nome do usuário
    pin = st.session_state.pin
    nome = authenticate_pin(pin)
    # Obter a hora atual
    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Criar nova linha com nome, botão e hora
    new_row = {"Name": nome, "Button": button_name, "SubmissionDateTime": submission_datetime}
    # Adicionar nova linha aos dados existentes
    new_rows = existing_data_reservations.to_dict(orient="records")
    new_rows.append(new_row)
    # Atualizar a planilha com os novos dados
    conn.update(worksheet="Folha", data=new_rows)
    st.success("Dados registrados com sucesso!")

# Página do relatório
def report_page():
    st.title("Relatório")
    # Filtrar os dados por nome e datas
    nome_filtro = st.sidebar.text_input("Filtrar por nome:")
    data_inicio = st.sidebar.date_input("Data de início:")
    data_fim = st.sidebar.date_input("Data de fim:")
    if data_inicio > data_fim:
        st.error("A data de início não pode ser posterior à data de fim.")
    else:
        filtered_data = existing_data_reservations.copy()
        if nome_filtro:
            filtered_data = filtered_data[filtered_data["Name"].str.contains(nome_filtro)]
        if data_inicio and data_fim:
            filtered_data = filtered_data[(filtered_data["SubmissionDateTime"] >= data_inicio) & (filtered_data["SubmissionDateTime"] <= data_fim)]
        st.write(filtered_data)

# Função para verificar se o PIN corresponde ao nome do usuário
def authenticate_pin(pin):
    dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
    if int(float(pin)) in dados["Pin"].tolist():
        return dados.loc[dados["Pin"] == int(float(pin)), "Nome"].iloc[0]
    else:
        return None

# Definir as páginas
pages = {
    "login_page": login_page,
    "buttons_page": buttons_page,
    "report_page": report_page
}

# Verificar a página atual
if "page" not in st.session_state:
    st.session_state.page = "login_page"

# Renderizar a página atual
current_page = pages[st.session_state.page]()
if current_page:
    st.session_state.page = current_page
