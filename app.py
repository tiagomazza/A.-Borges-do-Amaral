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

    # Escrever na planilha junto com outras informações
    conn.update(
        worksheet="Folha",  # Substituir pelo nome da sua planilha
        data=[{"Nome": nome, "Ação": acao, "Timestamp": hora_atual}]
    )

    st.success(f"Registro de '{acao}' efetuado com sucesso!")

# Interface do Streamlit
st.title("Registo de Ponto")

# Obtendo a lista de PINs e nomes do Google Sheets
pins_nomes = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
pins_nomes = pins_nomes.dropna(subset=["Pin", "Nome"])  # Remover linhas com valores ausentes

# Obtendo a lista de PINs disponíveis
pins_disponiveis = pins_nomes["Pin"].tolist()

# Adicionar campo de seleção de PIN
pin_selecionado = st.selectbox("PIN:", options=[""] + pins_disponiveis, format_func=lambda x: "" if x == "" else "*")

# Verificar se o PIN foi selecionado
if pin_selecionado:
    # Obter o nome correspondente ao PIN selecionado
    nome = pins_nomes.loc[pins_nomes["Pin"] == pin_selecionado, "Nome"].iloc[0]

    st.write(f"<h1>Bem-vindo, {nome}!</h1>", unsafe_allow_html=True)

    # Botões para as ações de registro
    if st.button("Entrada Manhã"):
        escrever_registro(nome, "entrada manhã")
    if st.button("Saída Manhã"):
        escrever_registro(nome, "saída manhã")
    if st.button("Entrada Tarde"):
        escrever_registro(nome, "entrada tarde")
    if st.button("Saída Tarde"):
        escrever_registro(nome, "saída tarde")
elif pin_selecionado == "":
    st.warning("Por favor, selecione um PIN.")
else:
    st.warning("PIN inválido. Por favor, selecione um PIN válido.")
