import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para buscar o nome pelo PIN no Google Sheets
def obter_nome_por_pin(pin_digitado):
    # Ler os dados do Google Sheets
    dados = conn.read("Dados", ttl=3600)  # Substitua "Dados" pelo nome da sua planilha

    # Procurar o PIN na coluna "Pin" e retornar o nome correspondente da coluna "Nomes"
    nome = dados[dados["Pin"] == pin_digitado]["Nome"].values.tolist()
    
    # Retorna o nome se encontrado, senão retorna uma string vazia
    return nome[0] if nome else ""

# Função para escrever o número 1 na planilha do Google Sheets
def escrever_numero(nome, botao, hora):
    # Definir o número a ser escrito
    numero = 1
    
    # Obter a hora atual para registro na planilha, se não for fornecida
    if not hora:
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Escrever o número na planilha junto com outras informações
    conn.update(
        worksheet="Folha",  # Substitua pelo nome da sua planilha
        data=[{"Nome": nome, "Botao": botao, "Numero": numero, "Timestamp": hora}]
    )

    st.success("Registo efetuado")

# Interface do Streamlit
st.title("Registo de Ponto")

# Obtendo a senha dos segredos
senha_secreta = st.secrets["senhas"]["senha2"]

# Adicionar campo de senha
senha_digitada = st.text_input("Digite o seu pin:", type="password")

# Verificar se o PIN está correto e obter o nome correspondente
if senha_digitada == senha_secreta:
    st.subheader("Registar Ponto:")

    # Buscar o nome pelo PIN
    nome = obter_nome_por_pin(senha_digitada)

    if nome:
        st.write(f"Bem-vindo, {nome}!")

        # Campos de entrada para o botão e hora
        botao = st.selectbox("Botão:", ["Opção 1", "Opção 2", "Opção 3", "Opção 4"])
        hora = st.text_input("Hora (Opcional):", value="", help="Formato: YYYY-MM-DD HH:MM:SS")

        # Botão para efetuar o registo quando clicado
        if st.button("Efetuar Registo"):
            escrever_numero(nome, botao, hora)
    else:
        st.warning("PIN não encontrado.")
else:
    st.warning("PIN incorreto. Por favor, tente novamente.")
