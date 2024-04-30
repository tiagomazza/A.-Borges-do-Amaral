import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para escrever o número 1 na planilha do Google Sheets
def escrever_numero():
    # Definir o número a ser escrito
    numero = 1
    
    # Obter a hora atual para registro na planilha
    hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ler os dados existentes na aba "Folha"
    existing_data = conn.read(worksheet="Folha", ttl=5)
    if existing_data is None:
        existing_data = pd.DataFrame(columns=["Número", "Timestamp"])
    else:
        existing_data = pd.DataFrame(existing_data)
        
    # Obter a última linha escrita
    last_row_index = existing_data.shape[0]
    
    # Criar um novo registro com o número e o timestamp
    new_row = {"Número": numero, "Timestamp": hora_atual}
    
    # Adicionar o novo registro na próxima linha abaixo da última linha escrita
    existing_data = existing_data.append(new_row, ignore_index=True)
    
    # Escrever os dados atualizados na planilha
    conn.update(worksheet="Folha", data=existing_data.to_dict(orient="records"))

    st.success("Número 1 foi escrito na planilha!")

# Interface do Streamlit
st.title("Aplicativo para Escrever na Planilha")

# Adicionar campo de PIN
pin_digitado = st.text_input("Digite o seu PIN:", type="password")

# Verificar se o PIN foi digitado
if pin_digitado:
    # Ler os dados da aba "Dados" para encontrar o nome correspondente ao PIN inserido
    dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
    
    # Verificar se o PIN está na lista de PINs válidos
    if int(float(pin_digitado)) in dados["Pin"].tolist():
        # Dar as boas-vindas utilizando o nome correspondente
        nome = dados.loc[dados["Pin"] == int(float(pin_digitado)), "Nome"].iloc[0]
        st.write(f"Bem-vindo, {nome}!")
        
        # Botão para escrever o número 1 na planilha quando clicado
        if st.button("Registrar Número 1 na Planilha"):
            escrever_numero()
    else:
        st.warning("PIN incorreto. Por favor, digite um PIN válido.")
