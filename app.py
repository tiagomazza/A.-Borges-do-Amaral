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

# Página inicial
def main():
    st.title("📝 Registro de Ponto")

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

            # Adiciona espaço entre a mensagem de boas-vindas e os botões
            st.write("")

            # Botões para cada tipo de registro
            if st.button("☕ Entrada Manhã"):
                registrar_ponto(nome, "Entrada Manhã")

            if st.button("🌮 Saída Manhã"):
                registrar_ponto(nome, "Saída Manhã")

            if st.button("🌄 Entrada Tarde"):
                registrar_ponto(nome, "Entrada Tarde")

            if st.button("😴 Saída Tarde"):
                registrar_ponto(nome, "Saída Tarde")

            # Adiciona espaço entre os botões e a próxima seção
            st.write("")
            st.write("---")
            st.write("")

            # Adiciona um link para a página do administrador
            st.write("🔒 [Acessar a página do administrador](/admin)")

        else:
            st.warning("PIN incorreto. Por favor, digite um PIN válido.")

def registrar_ponto(nome, acao):
    # Obter a hora atual
    submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Criar nova linha com nome, ação e hora
    new_row = {"Name": nome, "Button": acao, "SubmissionDateTime": submission_datetime}

    # Adicionar nova linha aos dados existentes
    new_rows = existing_data_reservations.to_dict(orient="records")
    new_rows.append(new_row)

    # Atualizar a planilha com os novos dados
    conn.update(worksheet="Folha", data=new_rows)

    st.success("Dados registrados com sucesso!")

# Página do administrador (protegida pelo PIN)
def admin_page():
    st.title("🔒 Página do Administrador")
    st.write("Bem-vindo à página do administrador! Aqui você pode visualizar e gerenciar os dados registrados.")

    # Adicione o código para visualizar e gerenciar os dados conforme necessário

# Configurar roteamento entre páginas
if st.session_state.page == "main":
    main()
elif st.session_state.page == "admin":
    admin_page()

# Adicionar menu lateral
st.sidebar.title("Menu")
page = st.sidebar.radio("Selecione uma página:", options=["Página Principal", "Página do Administrador"])
if page == "Página Principal":
    st.session_state.page = "main"
elif page == "Página do Administrador":
    st.session_state.page = "admin"
