import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para escrever na planilha do Google Sheets
def escrever_registro(nome, acao):
    # Definir a ação a ser registrada
    acao = acao.title()  # Converter a ação para o formato correto (inicial maiúscula)

    # Obter a hora atual para registro na planilha
    hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Obter a última linha vazia
    last_row = len(conn.read("Folha", usecols=["Nome"], ttl=5)) + 1

    # Escrever na última linha vazia
    conn.update(
        worksheet="Folha",  # Substituir pelo nome da sua planilha
        data=[{"Nome": nome, "Ação": acao, "Timestamp": hora_atual}],
        start_cell=f"A{last_row}"
    )

    st.success(f"Registro de '{acao}' efetuado com sucesso!")

# Interface do Streamlit
st.title("Registo de Ponto")

# Obtendo a lista de PINs e nomes do Google Sheets
pins_nomes = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
pins_nomes = pins_nomes.dropna(subset=["Pin", "Nome"])  # Remover linhas com valores ausentes

# Obtendo a lista de PINs disponíveis
pins_disponiveis = [int(pin) for pin in pins_nomes["Pin"].tolist()]

# Adicionar campo para digitar o PIN
pin_digitado = st.text_input("Digite o seu PIN:", type="number")

# Verificar se o PIN foi digitado
if pin_digitado:
    # Verificar se o PIN está na lista de PINs disponíveis
    if int(pin_digitado) in pins_disponiveis:
        # Obter o nome correspondente ao PIN digitado
        nome = pins_nomes.loc[pins_nomes
