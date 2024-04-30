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

# Obtendo a senha dos segredos
senha_secreta = st.secrets["senhas"]["senha2"]

# Adicionar campo de senha
senha_digitada = st.text_input("Digite o seu pin:", type="password")

# Verificar se a senha está correta
if senha_digitada == senha_secreta:
    st.subheader("Registar Ponto:")

    # Dicionário com pin como chave e nome como valor
    pin_para_nome = {
        "pin1": "Nome1",
        "pin2": "Nome2",
        "pin3": "Nome3",
        # Adicione mais pares pin-nome conforme necessário
    }

    # Obter o nome do usuário pelo pin
    nome = pin_para_nome.get(senha_digitada, "")

    if nome:
        st.write(f"Bem-vindo, {nome}!")

        # Campos de entrada para o botão e hora
        botao = st.selectbox("Botão:", ["Opção 1", "Opção 2", "Opção 3", "Opção 4"])
        hora = st.text_input("Hora (Opcional):", value="", help="Formato: YYYY-MM-DD HH:MM:SS")

        # Botão para efetuar o registo quando clicado
        if st.button("Efetuar Registo"):
            escrever_numero(nome, botao, hora)
    else:
        st.warning("Pin não encontrado.")
else:
    st.warning("Pin incorreto. Por favor, tente novamente.")
