import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados existentes da planilha
def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, ttl=5)
    return existing_data.dropna(how="all")

def fill_missing_data(data_frame):
    default_entry_morning = pd.Timestamp.now().replace(hour=9, minute=0, second=0)
    default_exit_morning = pd.Timestamp.now().replace(hour=12, minute=30, second=0)
    default_entry_afternoon = pd.Timestamp.now().replace(hour=14, minute=30, second=0)
    default_exit_afternoon = pd.Timestamp.now().replace(hour=18, minute=0, second=0)
    
    for index, row in data_frame.iterrows():
        if pd.isnull(row['Entrada Manhã']):
            data_frame.at[index, 'Entrada Manhã'] = default_entry_morning
        if pd.isnull(row['Saída Manhã']):
            data_frame.at[index, 'Saída Manhã'] = default_exit_morning
        if pd.isnull(row['Entrada Tarde']):
            data_frame.at[index, 'Entrada Tarde'] = default_entry_afternoon
        if pd.isnull(row['Saída Tarde']):
            data_frame.at[index, 'Saída Tarde'] = default_exit_afternoon

def save_to_new_sheet(df, sheet_name="exportado"):
    try:
        # Verifica se a aba já existe
        try:
            existing_data = conn.read(worksheet=sheet_name, ttl=5)
        except Exception:
            existing_data = None
        
        # Se não existir, cria a aba
        if existing_data is None:
            conn.create(worksheet=sheet_name)

        # Converte DataFrame para dicionário
        df_dict = df.to_dict(orient="records")
        print("DataFrame convertido para dicionário:", df_dict)  # Adicionado para depuração

        # Atualiza a aba com os dados
        conn.update(worksheet=sheet_name, data=df_dict)
        print("Dados atualizados na nova aba.")  # Adicionado para depuração

        st.success(f"Dados salvos na aba '{sheet_name}' com sucesso.")
    except Exception as e:
        st.error(f"Erro ao salvar dados na aba '{sheet_name}': {e}")
st.sidebar.image("https://aborgesdoamaral.pt/wp-content/uploads/2021/04/marca-de-75-anos.png", use_column_width=True)  # 
pagina_selecionada = st.sidebar.radio("", ["✍🏽Marcação de Ponto", "🔍Consultas", "🔐Restrito"])


dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)

admin_row = dados.loc[dados["Nome"] == "Admin"]
if not admin_row.empty:
    senha_admin = str(int(admin_row["Pin"].iloc[0]))
else:
    senha_admin = None



# Carregar dados existentes
existing_data_reservations = load_existing_data("Folha")

# Determinar qual página exibir com base na seleção do usuário
if pagina_selecionada == "✍🏽Marcação de Ponto":
    st.title("✍🏽Marcação de Ponto")
    # Adicionar campo de PIN
    pin_digitado = st.text_input("Digite o seu PIN:")

    # Verificar se o PIN foi digitado
    if str(pin_digitado):
        # Ler os dados da aba "Dados" para encontrar o nome correspondente ao PIN inserido
        dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
               
        # Verificar se o PIN está na lista de PINs válidos
        try:
            pin_int = int(float(pin_digitado))
            if pin_int in dados["Pin"].tolist():
                nome = dados.loc[dados["Pin"] == pin_int, "Nome"].iloc[0]
                
                # Dar as boas-vindas utilizando o nome correspondente
                st.write(f"😀 Bem-vindo, {nome}!")

                # Adicionar espaço entre a mensagem de boas-vindas e os botões
                st.write("")

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

                    st.success("Dados registrados com sucesso!")

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

                    st.success("Dados registrados com sucesso!")

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

                    st.success("Dados registrados com sucesso!")

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

                    st.success("Dados registrados com sucesso!")
            else:
                st.error("PIN inválido!")

            except ValueError:
            st.error("Entrada inválida para PIN!")


        else:
            st.warning("PIN incorreto. Por favor, digite um PIN válido.")


# Página inicial para entrada da senha
if st.sidebar.text_input("",type="password") == str(senha_admin):
    # Conteúdo das abas "Consultas" e "Admin" aqui
    if pagina_selecionada == "🔍Consultas":
        st.title("🔍Consulta")
        
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

        # Preencher dados faltantes com os horários padrão
        fill_missing_data(grouped_data)

        # Calcular o total trabalhado por dia
        grouped_data['Total trabalhado'] = np.nan
        for index, row in grouped_data.iterrows():
            if not (pd.isnull(row['Entrada Manhã']) or pd.isnull(row['Saída Manhã']) or pd.isnull(row['Entrada Tarde']) or pd.isnull(row['Saída Tarde'])):
                total_trabalhado = (row['Saída Manhã'] - row['Entrada Manhã']) + (row['Saída Tarde'] - row['Entrada Tarde'])
                grouped_data.at[index, 'Total trabalhado'] = total_trabalhado

        # Converter o total trabalhado para horas e minutos
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: x.total_seconds() / 3600 if pd.notnull(x) else 0)
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: '{:02.0f}:{:02.0f}'.format(*divmod(x * 60, 60)))

        # Converter as colunas de entrada e saída para o formato hh:mm
        grouped_data['Entrada Manhã'] = grouped_data['Entrada Manhã'].dt.strftime("%H:%M")
        grouped_data['Saída Manhã'] = grouped_data['Saída Manhã'].dt.strftime("%H:%M")
        grouped_data['Entrada Tarde'] = grouped_data['Entrada Tarde'].dt.strftime("%H:%M")
        grouped_data['Saída Tarde'] = grouped_data['Saída Tarde'].dt.strftime("%H:%M")

        # Exibir o DataFrame agrupado na página
        st.write(grouped_data)

        sheet_name = st.text_input("Digite o nome da nova aba:", "Nova_aba")
        if st.button("Salvar dados"):
            save_to_new_sheet(grouped_data)

    elif pagina_selecionada == "🔐Restrito":
      
        st.title("🔐Restrito")

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

        # Preencher dados faltantes com os horários padrão
        fill_missing_data(df)

        # Agrupar por data e nome para calcular o total trabalhado por dia
        grouped_data = df.groupby(['Data', 'Nome']).agg({
            'Entrada Manhã': 'first',
            'Saída Manhã': 'first',
            'Entrada Tarde': 'first',
            'Saída Tarde': 'first'
        }).reset_index()

        # Calcular o total trabalhado por dia
        grouped_data['Total trabalhado'] = np.nan
        for index, row in grouped_data.iterrows():
            if not (pd.isnull(row['Entrada Manhã']) or pd.isnull(row['Saída Manhã']) or pd.isnull(row['Entrada Tarde']) or pd.isnull(row['Saída Tarde'])):
                total_trabalhado = (row['Saída Manhã'] - row['Entrada Manhã']) + (row['Saída Tarde'] - row['Entrada Tarde'])
                grouped_data.at[index, 'Total trabalhado'] = total_trabalhado

        # Converter o total trabalhado para horas e minutos
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: x.total_seconds() / 3600 if pd.notnull(x) else 0)
        grouped_data['Total trabalhado'] = grouped_data['Total trabalhado'].apply(lambda x: '{:02.0f}:{:02.0f}'.format(*divmod(x * 60, 60)))

        # Converter as colunas de entrada e saída para o formato hh:mm
        grouped_data['Entrada Manhã'] = grouped_data['Entrada Manhã'].dt.strftime("%H:%M")
        grouped_data['Saída Manhã'] = grouped_data['Saída Manhã'].dt.strftime("%H:%M")
        grouped_data['Entrada Tarde'] = grouped_data['Entrada Tarde'].dt.strftime("%H:%M")
        grouped_data['Saída Tarde'] = grouped_data['Saída Tarde'].dt.strftime("%H:%M")

        # Exibir o DataFrame agrupado na página
        st.write(grouped_data)

        sheet_name = st.text_input("Digite o nome da nova aba:", "Nova_aba")
        if st.button("Salvar dados"):
            save_to_new_sheet(grouped_data)
else:
    st.warning("Pin incorreto.")