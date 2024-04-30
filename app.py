import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para escrever o número 1 na planilha do Google Sheets
def escrever_numero(nome, botao, hora):
    # Definir o número a ser escrito
    numero = 1
    
    # Obter a hora atual para registro na planilha, se não for fornecida
    if not hora:
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Escrever o número na planilha junto com outras informações
    conn.update(
        worksheet="Folha",  # Substituir pelo nome da sua planilha
        data=[{"Nome": nome, "Botao": botao, "Numero": numero, "Timestamp": hora}]
    )

    st.success("Registo efetuado")

# Interface do Streamlit
st.title("Registo de Ponto")

# Obtendo a lista de PINs e nomes do Google Sheets
pins_nomes = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
pins_nomes = pins_nomes.dropna(subset=["Pin", "Nome"])  # Remover linhas com valores ausentes

# Obtendo a lista de PINs disponíveis
pins_disponiveis = pins_nomes["Pin"].tolist()

# Adicionar campo de seleção de PIN
pin_selecionado = st.selectbox("Selecione o seu PIN:", options=[""] + pins_disponiveis)

# Verificar se o PIN foi selecionado
if pin_selecionado:
    # Obter o nome correspondente ao PIN selecionado
    nome = pins_nomes.loc[pins_nomes["Pin"] == pin_selecionado, "Nome"].iloc[0]

    st.write(f"Bem-vindo, {nome}!")

    # Campos de entrada para o botão e hora
    botao = st.selectbox("Botão:", ["Opção 1", "Opção 2", "Opção 3", "Opção 4"])
    hora = st.text_input("Hora (Opcional):", value="", help="Formato: YYYY-MM-DD HH:MM:SS")

    # Botão para efetuar o registo quando clicado
    if st.button("Efetuar Registo"):
        escrever_numero(nome, botao, hora)
elif pin_selecionado == "":
    st.warning("Por favor, selecione um PIN.")
else:
    st.warning("PIN inválido. Por favor, selecione um PIN válido.")
