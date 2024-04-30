import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para escrever o nome do botão na planilha do Google Sheets
def escrever_registro(nome, acao):
    # Obter a hora atual para registro na planilha
    hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ler os dados existentes da aba "Folha"
    existing_data = conn.read(worksheet="Folha", ttl=5)
    
    # Preparar os novos dados a serem adicionados
    new_data = {"Nome": nome, "Ação": acao, "Timestamp": hora_atual}
    
    # Adicionar a nova entrada aos dados existentes
    existing_data.append(new_data)
    
    # Atualizar a planilha com todas as informações
    conn.update(worksheet="Folha", data=existing_data)
    
    st.success(f"Registro de '{acao}' realizado para {nome}!")

# Interface do Streamlit
st.title("Registro de Ponto")

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
        st.write(f"Bem-vindo, {nome}!")
        
        st.subheader("Botões disponíveis:")
        
        # Botões para registrar as ações
        if st.button("Entrada Manhã"):
            escrever_registro(nome, "Entrada Manhã")
        if st.button("Saída Manhã"):
            escrever_registro(nome, "Saída Manhã")
        if st.button("Entrada Tarde"):
            escrever_registro(nome, "Entrada Tarde")
        if st.button("Saída Tarde"):
            escrever_registro(nome, "Saída Tarde")
    else:
        st.warning("PIN incorreto. Por favor, digite um PIN válido.")
