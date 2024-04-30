import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para escrever o número 1 na planilha do Google Sheets
def escrever_numero(nome):
    # Definir o número a ser escrito
    numero = 1
    
    # Obter a hora atual para registro na planilha
    hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Escrever o número na planilha
    conn.append(
        worksheet="Folha",  # Substituir pelo nome da sua planilha
        data=[[nome, numero, hora_atual]],
        start='A1',  # A partir da primeira linha da planilha
        dimension='ROWS'  # Adiciona como nova linha
    )

    st.success(f"Número 1 foi escrito na planilha para {nome}!")

# Interface do Streamlit
st.title("Aplicativo para Escrever na Planilha")

# Adicionar campo de PIN
pin_digitado = st.text_input("Digite o seu PIN:")

# Verificar se o PIN foi digitado
if pin_digitado:
    # Ler os dados da aba "Dados" para encontrar o nome correspondente ao PIN inserido
    dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
    
    # Verificar se o PIN está na lista de PINs válidos
    if int(pin_digitado) in dados["Pin"].tolist():
        nome = dados.loc[dados["Pin"] == int(pin_digitado), "Nome"].iloc[0]
        
        # Dar as boas-vindas utilizando o nome correspondente
        st.write(f"Bem-vindo, {nome}!")
        
        st.subheader("Botões disponíveis:")
        
        # Botão para escrever o número 1 na planilha quando clicado
        if st.button("Escrever Número 1 na Planilha"):
            escrever_numero(nome)
    else:
        st.warning("PIN incorreto. Por favor, digite um PIN válido.")
