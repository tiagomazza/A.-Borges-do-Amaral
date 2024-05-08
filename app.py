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

# Função para adicionar entrada/saída
def add_entry(button, name):
    # Verificar se já existe um registro para o mesmo usuário, botão e data
    today_date = pd.Timestamp.now().strftime("%Y-%m-%d")
    if existing_data_reservations[(existing_data_reservations["Name"] == name) & 
                                  (existing_data_reservations["Button"] == button) & 
                                  (existing_data_reservations["SubmissionDateTime"].dt.strftime("%Y-%m-%d") == today_date)].empty:
        # Obter a hora atual
        submission_datetime = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Criar nova linha com nome, botão e hora
        new_row = {"Name": name, "Button": button, "SubmissionDateTime": submission_datetime}

        # Adicionar nova linha aos dados existentes
        new_rows = existing_data_reservations.to_dict(orient="records")
        new_rows.append(new_row)

        # Atualizar a planilha com os novos dados
        conn.update(worksheet="Folha", data=new_rows)

        st.success("Dados registrados com sucesso!")
    else:
        st.warning("Registro já efetuado para este usuário, botão e data.")

# Função para adicionar a data atual aos dados faltantes
def add_current_date_to_missing_data(data_frame):
    current_date = pd.Timestamp.now().strftime("%Y-%m-%d")
    for index, row in data_frame.iterrows():
        if pd.isnull(row['SubmissionDateTime']):
            data_frame.at[index, 'SubmissionDateTime'] = current_date

    # Atualizar a planilha com os novos dados
    conn.update(worksheet="Folha", data=data_frame.to_dict(orient="records"))
    st.success("Datas faltantes adicionadas com sucesso.")

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

            # Botões para cada tipo de registro
            if st.button("☕ Entrada Manhã"):
                add_entry("Entrada Manhã", nome)

            if st.button("🌮 Saída Manhã"):
                add_entry("Saída Manhã", nome)

            if st.button("🌄 Entrada Tarde"):
                add_entry("Entrada Tarde", nome)

            if st.button("😴 Saída Tarde"):
                add_entry("Saída Tarde", nome)

        else:
            st.warning("PIN incorreto. Por favor, digite um PIN válido.")

elif pagina_selecionada == "Consultas":
    st.title("Consulta de Registros")
    
    # Botão para adicionar a data atual aos dados faltantes
    if st.button("Adicionar data atual aos dados faltantes"):
        add_current_date_to_missing_data(existing_data_reservations)

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
    df['Entrada Manhã'] = pd.to_datetime(df['Entrada Manhã'])
    df['Saída Manhã'] = pd.to_datetime(df['Saída Manhã'])
    df['Entrada Tarde'] = pd.to_datetime(df['Entrada Tarde'])
    df['Saída Tarde'] = pd.to_datetime(df['Saída Tarde'])

    # Agrupar por data e nome para calcular o total trabalhado por dia
    grouped_data = df.groupby(['Data', 'Nome']).agg({
        'Entrada Manhã': 'first',
        'Saída Manhã': 'first',
        'Entrada Tarde': 'first',
        'Saída Tarde': 'first'
    }).reset_index()

    # Calcular o total trabalhado por dia
    for index, row in grouped_data.iterrows():
        if not (pd.isnull(row['Entrada Manhã']) or pd.isnull(row['Saída Manhã']) or pd.isnull(row['Entrada Tarde']) or pd.isnull(row['Saída Tarde'])):
            total_trabalhado = (row['Saída Manhã'] - row['Entrada Manhã']) + (row['Saída Tarde'] - row['Entrada Tarde'])
            grouped_data.at[index, 'Total trabalhado'] = total_trabalhado
        else:
            grouped_data.at[index, 'Total trabalhado'] = np.nan

    # Converter o total trabalhado para horas e minutos
    grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].dt.total_seconds() / 3600
    grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: '{:02.0f}:{:02.0f}'.format(*divmod(x * 60, 60)))

    # Converter as colunas de entrada e saída para o formato hh:mm
    grouped_data['Entrada Manhã'] = grouped_data['Entrada Manhã'].dt.strftime("%H:%M")
    grouped_data['Saída Manhã'] = grouped_data['Saída Manhã'].dt.strftime("%H:%M")
    grouped_data['Entrada Tarde'] = grouped_data['Entrada Tarde'].dt.strftime("%H:%M")
    grouped_data['Saída Tarde'] = grouped_data['Saída Tarde'].dt.strftime("%H:%M")

    # Exibir o DataFrame agrupado na página
    st.write(grouped_data)
