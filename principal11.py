import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# ——————————————————————————————————————————————————————————————
# 1) Fuso horário local (ex.: São Paulo)
fuso = pytz.timezone('America/Sao_Paulo')

# 2) Carregar e normalizar colaboradores
try:
    colaboradores = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()
except Exception as e:
    st.error(f"Erro ao ler 'colaboradores.csv': {e}")
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

# 3) Carregar e normalizar ferramentas
try:
    ferramentas = pd.read_csv('ferramentas.csv', encoding='utf-8-sig')
    ferramentas.columns = ferramentas.columns.str.strip()
    ferramentas.rename(columns={'Descrição': 'Descricao'}, inplace=True)
except Exception as e:
    st.error(f"Erro ao ler 'ferramentas.csv': {e}")
    ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao'])

# ——————————————————————————————————————————————————————————————
# Configuração geral da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Ferramentaria")

# Menu lateral
menu = st.sidebar.radio(
    "Menu",
    ["Movimentação", "Colaborador", "Ferramenta", "Relatório"]
)

if menu == "Movimentação":
    st.header("Movimentação")

    # Formulário com reset automático
    with st.form("movimentacao_form", clear_on_submit=True):
        # Matrícula e lookup de nome
        matricula = st.text_input("Matrícula")
        nome = ""
        if matricula:
            df_col = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
            nome = df_col['Nome'].values[0] if not df_col.empty else "Matrícula não encontrada"
        st.text_input("Nome", value=nome, disabled=True)

        # Tipo de movimentação
        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])

        # Quantidade de Ferramentas
        qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)

        selecionadas = []
        for i in range(qtd):
            with st.expander(f"Ferramenta {i+1}"):
                codigo = st.text_input(f"Código da Ferramenta {i+1}")
                desc = ""
                if codigo:
                    df_f = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                    desc = df_f['Descricao'].values[0] if not df_f.empty else "Código não encontrado"
                st.text_input(f"Descrição {i+1}", value=desc, disabled=True)
                selecionadas.append((codigo, desc))

        # Observações
        observacoes = st.text_area("Observações (opcional)")

        # Botão de submit
        submitted = st.form_submit_button("Confirmar Movimentação")

        if submitted:
            # 1) Salvar em CSV
            agora = datetime.now(fuso)
            datahora = agora.strftime('%d/%m/%Y %H:%M:%S')
            ferramentas_str = "; ".join(f"{c} - {d}" for c, d in selecionadas)
            file_path = 'movimentacoes.csv'
            header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
            new_row = [datahora, matricula, nome, tipo, ferramentas_str, observacoes]
            write_header = not os.path.exists(file_path)
            with open(file_path, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                if write_header:
                    writer.writerow(header)
                writer.writerow(new_row)

            st.success("Movimentação registrada com sucesso!")

elif menu == "Relatório":
    st.header("Relatório de Movimentações")
    try:
        df_mov = pd.read_csv('movimentacoes.csv', encoding='utf-8-sig')
        st.dataframe(df_mov)
    except FileNotFoundError:
        st.info("Ainda não há movimentações registradas.")

elif menu == "Colaborador":
    st.header("Colaborador")
    st.info("Página em construção.")

elif menu == "Ferramenta":
    st.header("Ferramenta")
    st.info("Página em construção.")
