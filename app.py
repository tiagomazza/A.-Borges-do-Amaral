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

pagina_selecionada = st.sidebar.radio("Acessos", ["Marcação de Ponto", "Consultas"])

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
                register_button_click("Entrada Manhã", nome)

            if st.button("🌮 Saída Manhã"):
                register_button_click("Saída Manhã", nome)

            if st.button("🌄 Entrada Tarde"):
                register_button_click("Entrada Tarde", nome)

            if st.button("😴 Saída Tarde"):
                register_button_click("Saída Tarde", nome)

        else:
            st.warning("PIN incorreto. Por favor, digite um PIN válido.")

else:
    st.title("Consultas")

    # Filtro por data
    data_inicio = st.sidebar.date_input("Data de início:")
    data_fim = st.sidebar.date_input("Data de fim:")
    
    # Filtro por nome
    nome_filtro = st.sidebar.selectbox("Filtrar por nome:", nomes_disponiveis)

    # Converter as strings de data para objetos datetime.date
    data_inicio = datetime.combine(data_inicio, datetime.min.time()) if data_inicio else None
    data_fim = datetime.combine(data_fim, datetime.max.time()) if data_fim else None

    # Filtrar os dados
    filtered_data = existing_data_reservations.copy()
    if data_inicio and data_fim:
        filtered_data["SubmissionDateTime"] = pd.to_datetime(filtered_data["SubmissionDateTime"])
        filtered_data = filtered_data[(filtered_data["SubmissionDateTime"] >= data_inicio) & (filtered_data["SubmissionDateTime"] <= data_fim)]
    if nome_filtro:
        filtered_data = filtered_data[filtered_data["Name"].str.contains(nome_filtro)]

    # Exibir os dados filtrados
    st.write(filtered_data)

# Função para registrar o clique em um botão na planilha
def register_button_click(button_name, nome):
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
