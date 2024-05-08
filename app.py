
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

            # Botões para cada tipo de registro
            if st.button("☕ Entrada Manhã"):
                # Obter a hora atual
                submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Criar nova linha com nome, botão e hora
                new_row = {"Name": nome, "Button": "Entrada Manhã", "SubmissionDateTime": submission_datetime}

                # Adicionar nova linha aos dados existentes
                new_rows = existing_data_reservations.to_dict(orient="records")
                new_rows.append(new_row)

                # Atualizar a planilha com os novos dados
                conn.update(worksheet="Folha", data=new_rows)

                st.success("Dados registados com sucesso!")

            if st.button("🌮 Saída Manhã"):
                # Obter a hora atual
                submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Criar nova linha com nome, botão e hora
                new_row = {"Name": nome, "Button": "Saída Manhã", "SubmissionDateTime": submission_datetime}

                # Adicionar nova linha aos dados existentes
                new_rows = existing_data_reservations.to_dict(orient="records")
                new_rows.append(new_row)

                # Atualizar a planilha com os novos dados
                conn.update(worksheet="Folha", data=new_rows)

                st.success("Dados registados com sucesso!")

            if st.button("🌄 Entrada Tarde"):
                # Obter a hora atual
                submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Criar nova linha com nome, botão e hora
                new_row = {"Name": nome, "Button": "Entrada Tarde", "SubmissionDateTime": submission_datetime}

                # Adicionar nova linha aos dados existentes
                new_rows = existing_data_reservations.to_dict(orient="records")
                new_rows.append(new_row)

                # Atualizar a planilha com os novos dados
                conn.update(worksheet="Folha", data=new_rows)

                st.success("Dados registados com sucesso!")

            if st.button("😴 Saída Tarde"):
                # Obter a hora atual
                submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Criar nova linha com nome, botão e hora
                new_row = {"Name": nome, "Button": "Saída Tarde", "SubmissionDateTime": submission_datetime}

                # Adicionar nova linha aos dados existentes
                new_rows = existing_data_reservations.to_dict(orient="records")
                new_rows.append(new_row)

                # Atualizar a planilha com os novos dados
                conn.update(worksheet="Folha", data=new_rows)

                st.success("Dados registados com sucesso!")

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

    # Agrupar por data e nome para calcular o total trabalhado por dia
    df = pd.DataFrame(data)
    df['Entrada Manhã'] = pd.to_datetime(df['Entrada Manhã'], format="%H:%M")
    df['Saída Manhã'] = pd.to_datetime(df['Saída Manhã'], format="%H:%M")
    df['Entrada Tarde'] = pd.to_datetime(df['Entrada Tarde'], format="%H:%M")
    df['Saída Tarde'] = pd.to_datetime(df['Saída Tarde'], format="%H:%M")

    # Agrupar linhas com mesma Data e Nome
    df = df.groupby(['Data', 'Nome'], as_index=False).agg(lambda x: next(iter(x.dropna()), np.nan))

    df['Entrada Manhã conv'] = df['Entrada Manhã'].dt.hour * 60 + df['Entrada Manhã'].dt.minute
    df['Saída Manhã conv'] = df['Saída Manhã'].dt.hour * 60 + df['Saída Manhã'].dt.minute
    df['Entrada Tarde conv'] = df['Entrada Tarde'].dt.hour * 60 + df['Entrada Tarde'].dt.minute
    df['Saída Tarde conv'] = df['Saída Tarde'].dt.hour * 60 + df['Saída Tarde'].dt.minute
    df['Total trabalhado calc'] = df['Saída Manhã conv']- df['Entrada Manhã conv'] + df['Saída Tarde conv']- df['Entrada Tarde conv']
    df['Total trabalhado'] = pd.to_datetime(df['Total trabalhado calc'], unit='m').dt.strftime('%H:%M')

    #df.drop(columns=['Entrada Manhã conv', 'Saída Manhã conv', 'Entrada Tarde conv', 'Saída Tarde conv', 'Total trabalhado calc' ], inplace=True)

    # Exibir o DataFrame na página
    st.write(df)