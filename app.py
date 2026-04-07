import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo

TZ_PT = ZoneInfo("Europe/Lisbon")

st.set_page_config(page_title="Marcação de Ponto", layout="wide")

st.markdown(
    """
    <style>
    .stTextInput>div>div>input {
        background-color: #ffcccb;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

conn = st.connection("gsheets", type=GSheetsConnection)

def now_pt():
    return datetime.now(TZ_PT)

def today_pt():
    return now_pt().date()

def load_existing_data(worksheet_name):
    try:
        existing_data = conn.read(worksheet=worksheet_name, ttl=5)
        return existing_data.dropna(how="all")
    except Exception:
        return pd.DataFrame()

def fill_missing_data(data_frame):
    default_entry_morning = pd.Timestamp.combine(date.today(), time(9, 0))
    default_exit_morning = pd.Timestamp.combine(date.today(), time(12, 30))
    default_entry_afternoon = pd.Timestamp.combine(date.today(), time(14, 30))
    default_exit_afternoon = pd.Timestamp.combine(date.today(), time(18, 0))

    for index, row in data_frame.iterrows():
        if pd.isnull(row["Entrada Manhã"]):
            data_frame.at[index, "Entrada Manhã"] = default_entry_morning
        if pd.isnull(row["Saída Manhã"]):
            data_frame.at[index, "Saída Manhã"] = default_exit_morning
        if pd.isnull(row["Entrada Tarde"]):
            data_frame.at[index, "Entrada Tarde"] = default_entry_afternoon
        if pd.isnull(row["Saída Tarde"]):
            data_frame.at[index, "Saída Tarde"] = default_exit_afternoon

def save_to_new_sheet(df, sheet_name):
    try:
        try:
            conn.read(worksheet=sheet_name, ttl=5)
        except Exception:
            conn.create(worksheet=sheet_name)

        conn.update(worksheet=sheet_name, data=df)
        st.success(f"Dados salvos na aba '{sheet_name}' com sucesso.")
    except Exception as e:
        st.error(f"Erro ao salvar dados na aba '{sheet_name}': {e}")

def append_row_to_sheet(conn, worksheet, row_values):
    df = conn.read(worksheet=worksheet, ttl=5)
    real_column_order = df.columns.tolist()
    df = df.dropna(how="all").reset_index(drop=True)
    new_row = list(row_values)
    while len(new_row) < len(real_column_order):
        new_row.append(np.nan)
    df.loc[len(df)] = new_row[:len(real_column_order)]
    df = df[real_column_order]
    conn.update(worksheet=worksheet, data=df)

def parse_submission_datetime(series):
    dt = pd.to_datetime(series, errors="coerce")
    return dt

def build_daily_summary(filtered_data, fill_defaults=False):
    df = filtered_data.copy()
    df["SubmissionDateTime"] = parse_submission_datetime(df["SubmissionDateTime"])
    df = df.dropna(subset=["SubmissionDateTime"])

    df["Data"] = df["SubmissionDateTime"].dt.strftime("%d/%m")
    df["Hora"] = df["SubmissionDateTime"].dt.strftime("%H:%M")

    data = {
        "Data": df["Data"],
        "Nome": df["Name"],
        "Entrada Manhã": np.where(df["Button"] == "Entrada Manhã", df["Hora"], pd.NaN),
        "Saída Manhã": np.where(df["Button"] == "Saída Manhã", df["Hora"], pd.NaN),
        "Entrada Tarde": np.where(df["Button"] == "Entrada Tarde", df["Hora"], pd.NaN),
        "Saída Tarde": np.where(df["Button"] == "Saída Tarde", df["Hora"], pd.NaN),
    }

    out = pd.DataFrame(data)
    for c in ["Entrada Manhã", "Saída Manhã", "Entrada Tarde", "Saída Tarde"]:
        out[c] = pd.to_datetime(out[c], format="%H:%M", errors="coerce")

    if fill_defaults:
        fill_missing_data(out)

    grouped_data = out.groupby(["Data", "Nome"], as_index=False).agg({
        "Entrada Manhã": "first",
        "Saída Manhã": "first",
        "Entrada Tarde": "first",
        "Saída Tarde": "first"
    })

    totals = []
    for _, row in grouped_data.iterrows():
        if pd.notnull(row["Entrada Manhã"]) and pd.notnull(row["Saída Manhã"]) and pd.notnull(row["Entrada Tarde"]) and pd.notnull(row["Saída Tarde"]):
            total = (row["Saída Manhã"] - row["Entrada Manhã"]) + (row["Saída Tarde"] - row["Entrada Tarde"])
            totals.append(total)
        else:
            totals.append(pd.NaT)

    grouped_data["Total trabalhado"] = totals

    def fmt_total(x):
        if pd.isnull(x):
            return "00:00"
        minutes = int(x.total_seconds() // 60)
        h, m = divmod(minutes, 60)
        return f"{h:02d}:{m:02d}"

    grouped_data["Total trabalhado"] = grouped_data["Total trabalhado"].apply(fmt_total)

    for c in ["Entrada Manhã", "Saída Manhã", "Entrada Tarde", "Saída Tarde"]:
        grouped_data[c] = grouped_data[c].dt.strftime("%H:%M")

    return grouped_data

st.sidebar.image(
    "https://aborgesdoamaral.pt/wp-content/uploads/2021/04/marca-de-75-anos.png",
    width=180
)

pagina_selecionada = st.sidebar.radio(
    "Menu",
    ["✍🏽Marcação de Ponto", "🔍Consultas", "🔐Restrito"],
    label_visibility="hidden"
)

try:
    dados = conn.read(worksheet="Dados", usecols=["Pin", "Nome"], ttl=5)
except Exception:
    dados = pd.DataFrame(columns=["Pin", "Nome"])

admin_row = dados.loc[dados["Nome"] == "Admin"] if not dados.empty else pd.DataFrame()
senha_admin = str(int(admin_row["Pin"].iloc[0])) if not admin_row.empty else None

try:
    existing_data_reservations = load_existing_data("Folha")
    if not existing_data_reservations.empty and existing_data_reservations.shape[1] >= 3:
        existing_data_reservations = existing_data_reservations.iloc[:, :3]
        existing_data_reservations.columns = ["Name", "Button", "SubmissionDateTime"]
    else:
        existing_data_reservations = pd.DataFrame(columns=["Name", "Button", "SubmissionDateTime"])
except Exception:
    existing_data_reservations = pd.DataFrame(columns=["Name", "Button", "SubmissionDateTime"])

if pagina_selecionada == "✍🏽Marcação de Ponto":
    st.title("✍🏽 Marcação de Ponto")
    pin_digitado = st.text_input("Digite o seu PIN:", type="password")

    if pin_digitado:
        try:
            pin_int = int(float(pin_digitado))
            if not dados.empty and pin_int in dados["Pin"].tolist():
                nome = dados.loc[dados["Pin"] == pin_int, "Nome"].iloc[0]
                st.write(f"😀 Bem-vindo, **{nome}**!")
                st.write("👇🏽 Carregue no botão abaixo correspondente ao registo desejado:")

                def registar(button_name):
                    current_time = now_pt()
                    submission_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    advise_datetime = current_time.strftime("%H:%M")
                    append_row_to_sheet(conn, "Folha", [nome, button_name, submission_datetime])
                    st.success(f"Dados registados com sucesso às {advise_datetime}")

                if st.button("☕ Entrada Manhã"):
                    registar("Entrada Manhã")
                if st.button("🌮 Saída Manhã"):
                    registar("Saída Manhã")
                if st.button("🌄 Entrada Tarde"):
                    registar("Entrada Tarde")
                if st.button("😴 Saída Tarde"):
                    registar("Saída Tarde")
            else:
                st.warning("PIN incorreto.")
        except ValueError:
            st.warning("Utilize somente números.")

    else:
        st.info("Digite o PIN para continuar.")

try:
    entered_password_raw = st.sidebar.text_input("Digite sua senha:", type="password")
    entered_password = str(int(entered_password_raw)) if entered_password_raw else ""

    if pagina_selecionada in ["🔍Consultas", "🔐Restrito"]:
        if entered_password != senha_admin:
            st.warning("Acesso restrito. Insira a senha correta.")
        else:
            st.title("🔍Consulta" if pagina_selecionada == "🔍Consultas" else "🔐Restrito")

            if existing_data_reservations.empty:
                st.error("A planilha não possui dados para análise.")
                st.stop()

            nomes = existing_data_reservations["Name"].dropna().unique().tolist()
            filtro_nome = st.selectbox("Filtrar por Nome", ["Todos"] + nomes)
            data_inicio = st.date_input("Data de Início", value=today_pt())
            data_fim = st.date_input("Data de Fim", value=today_pt())

            filtered_data = existing_data_reservations.copy()
            filtered_data["SubmissionDateTime"] = pd.to_datetime(filtered_data["SubmissionDateTime"], errors="coerce")
            filtered_data = filtered_data.dropna(subset=["SubmissionDateTime"])

            if filtro_nome != "Todos":
                filtered_data = filtered_data[filtered_data["Name"] == filtro_nome]

            data_inicio_dt = datetime.combine(data_inicio, datetime.min.time())
            data_fim_dt = datetime.combine(data_fim, datetime.max.time())
            filtered_data = filtered_data[
                (filtered_data["SubmissionDateTime"] >= data_inicio_dt) &
                (filtered_data["SubmissionDateTime"] <= data_fim_dt)
            ]

            if filtered_data.empty:
                st.warning("Nenhum dado encontrado para os filtros selecionados.")
            else:
                grouped_data = build_daily_summary(
                    filtered_data,
                    fill_defaults=(pagina_selecionada == "🔐Restrito")
                )
                st.write(grouped_data)

                sheet_name = st.text_input("Digite o nome da nova aba:", "Nova_aba")
                if st.button("Salvar dados"):
                    save_to_new_sheet(grouped_data, sheet_name)

            st.write("[Aceder a planilha](https://docs.google.com/spreadsheets/d/1ujI1CUkvZoAYuucX4yrV2Z5BN3Z8-o-Kqm3PAfMqi0I/edit?gid=1541275584#gid=1541275584)")
            st.write("[Aceder a documentação](https://docs.google.com/document/d/1wgndUW2Xb48CBi6BSgSBRVw2sdqgqFtZxg_9Go5GYLg/edit?usp=sharing)")
except ValueError:
    st.warning("Senha inválida. Utilize apenas números.")
