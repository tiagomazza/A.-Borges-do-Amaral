import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para escrever na planilha do Google Sheets
def escrever_registro(nome, acao):
    # Obter o timestamp atual
    timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ler os dados existentes da aba "Dados" para encontrar o nome correspondente ao PIN inserido
    dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
    
    # Encontrar o nome correspondente ao PIN inserido
    nome = dados.loc[dados["Pin"] == int(pin_digitado), "Nome"].iloc[0]

    st.success(f"Registro de '{acao}' para '{nome}' efetuado com sucesso!")

# Interface do Streamlit
st.title("Registo de Ponto")

# Adicionar campo de entrada de PIN
pin_digitado = st.text_input("Digite o seu PIN:")

# Verificar se o PIN foi digitado
if pin_digitado:
    # Botões para as ações de registro
    if st.button("Entrada Manhã"):
        escrever_registro(pin_digitado, "Entrada Manhã")
    if st.button("Saída Manhã"):
        escrever_registro(pin_digitado, "Saída Manhã")
    if st.button("Entrada Tarde"):
        escrever_registro(pin_digitado, "Entrada Tarde")
    if st.button("Saída Tarde"):
        escrever_registro(pin_digitado, "Saída Tarde")
