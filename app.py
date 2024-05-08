import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd
import numpy as np

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados existentes da planilha
def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, ttl=5)
    return existing_data.dropna(how="all")

# Carregar dados existentes
existing_data_reservations = load_existing_data("Folha")

pagina_selecionada = st.sidebar.radio("Acessos", ["Marcação de Ponto", "Consultas"])

# Determinar qual página exibir com base na seleção do usuário
if pagina_selecionada == "Marcação de Ponto":

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

            # Adicionar espaço entre a mensagem de boas-vindas e os botões
            st.write("")

            buttons = {
            "☕ Entrada Manhã": "Entrada Manhã",
            "🌮 Saída Manhã": "Saída Manhã",
            "🌄 Entrada Tarde": "Entrada Tarde",
            "😴 Saída Tarde": "Saída Tarde"
            }

            for button_text, button_name in buttons.items():
                if st.button(button_text):
                    # Verificar se já existe um registro para este botão no mesmo dia
                    if existing_data_reservations[(existing_data_reservations['Nome'] == nome) & (existing_data_reservations[button_name] == button_name)].empty:
                        # Obter a hora atual
                        submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Criar nova linha com nome, botão, hora e data
                        new_row = {"Data": datetime.now().strftime("%d/%m%aa"), "Nome": nome, "Entrada Manhã", "Saída Manhã", "Entrada Tarde","Saída Tarde"  }

                        # Adicionar nova linha aos dados existentes
                        new_rows = existing_data_reservations.to_dict(orient="records")
                        new_rows.append(new_row)

                        # Atualizar a planilha com os novos dados
                        conn.update(worksheet="Folha", data=new_rows)

                        st.success("Dados registados com sucesso!")
                    else:
                        st.warning(f"Já foi registrado um(a) {button_name} para este usuário hoje.")

        else:
            st.warning("PIN incorreto. Por favor, digite um PIN válido.")

elif pagina_selecionada == "Consultas":
    st.title("Consulta de Registros")
    
    # Filtrar por nome
    nomes = existing_data_reservations["Name"].unique()
    filtro_nome = st.selectbox("Filtrar por Nome", ["Todos"] + list(nomes))

    # Filtrar por data
    data_inicio = st.date_input("Data de Início")
    data_fim = st.date_input("Data de Fim")

    # Filtrar os dados
    filtered_data = existing_data_reservations.copy()

    if filtro_nome != "Todos":
        filtered_data = filtered_data[filtered_data["Name"] == filtro_nome]

    if data_inicio and data_fim:
        data_inicio = datetime.combine(data_inicio, datetime.min.time())
        data_fim = datetime.combine(data_fim, datetime.max.time())
        filtered_data["SubmissionDateTime"] = pd.to_datetime(filtered_data["SubmissionDateTime"])
        filtered_data = filtered_data[(filtered_data["SubmissionDateTime"] >= data_inicio) & (filtered_data["SubmissionDateTime"] <= data_fim)]

    # Criar DataFrame com os dados filtrados
# Criar DataFrame com os dados filtrados
    data = {
        'Data': filtered_data['SubmissionDateTime'].dt.strftime("%d/%m"),  # Formatando para dd/mm
        'Nome': filtered_data['Name'],
        'Entrada Manhã': np.where(filtered_data['Button'] == 'Entrada Manhã', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
        'Saída Manhã': np.where(filtered_data['Button'] == 'Saída Manhã', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
        'Entrada Tarde': np.where(filtered_data['Button'] == 'Entrada Tarde', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
        'Saída Tarde': np.where(filtered_data['Button'] == 'Saída Tarde', filtered_data['SubmissionDateTime'].dt.strftime("%H:%M"), pd.NaT),
        'Total trabalhado': pd.NaT
    }

    df = pd.DataFrame(data)
    df['Entrada Manhã'] = pd.to_datetime(df['Entrada Manhã'], format="%H:%M")
    df['Saída Manhã'] = pd.to_datetime(df['Saída Manhã'], format="%H:%M")
    df['Entrada Tarde'] = pd.to_datetime(df['Entrada Tarde'], format="%H:%M")
    df['Saída Tarde'] = pd.to_datetime(df['Saída Tarde'], format="%H:%M")

    # Agrupar por data e nome para calcular o total trabalhado por dia
    grouped_data = df.groupby(['Data', 'Nome']).agg({
    'Entrada Manhã': 'first',
    'Saída Manhã': 'first',
    'Entrada Tarde': 'first',
    'Saída Tarde': 'first'
    }).reset_index()

    # Calcular o total trabalhado por dia
    grouped_data['Total trabalhado'] = (grouped_data['Saída Manhã'] - grouped_data['Entrada Manhã']) + (grouped_data['Saída Tarde'] - grouped_data['Entrada Tarde'])

    # Exibir o DataFrame agrupado na página
    st.write(grouped_data)