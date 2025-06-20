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

# 4) Garantir que exista o arquivo de movimentações com cabeçalho
mov_file = 'movimentacoes.csv'
mov_header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
if not os.path.exists(mov_file):
    pd.DataFrame(columns=mov_header).to_csv(mov_file, index=False, encoding='utf-8-sig')

# ——————————————————————————————————————————————————————————————
# Configuração da página
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

# ——————————————————————————————————————————————————————————————
if menu == "Movimentação":
    st.header("Movimentação")

    # Formulário com clear_on_submit
    with st.form("form_mov", clear_on_submit=True):
        matricula = st.text_input("Matrícula", key="matricula")
        nome = ""
        if matricula:
            df_col = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
            if not df_col.empty:
                nome = df_col['Nome'].values[0]
        st.text_input("Nome", value=nome, disabled=True)

        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"], key="tipo")
        qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1, key="qtd")

        selecionadas = []
        for i in range(st.session_state.qtd):
            with st.expander(f"Ferramenta {i+1}"):
                codigo = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")
                desc = ""
                if codigo:
                    df_f = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                    if not df_f.empty:
                        desc = df_f['Descricao'].values[0]
                st.text_input(f"Descrição {i+1}", value=desc, disabled=True, key=f"desc{i}")
                selecionadas.append((codigo, desc))

        observacoes = st.text_area("Observações (opcional)", key="obs")
        submit = st.form_submit_button("Confirmar Movimentação")

        if submit:
            # Somente após clicar aparecerão erros
            if not nome:
                st.error("Informe uma matrícula válida antes de registrar.")
            else:
                valid = [(c,d) for c,d in selecionadas if c and d]
                if not valid:
                    st.error("Informe pelo menos uma ferramenta válida antes de registrar.")
                else:
                    agora = datetime.now(fuso)
                    datahora = agora.strftime('%d/%m/%Y %H:%M:%S')
                    tools_str = "; ".join(f"{c} - {d}" for c,d in valid)
                    row = [datahora, matricula, nome, tipo, tools_str, observacoes]
                    with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
                    st.success("Movimentação registrada com sucesso!")

elif menu == "Colaborador":
    st.header("Colaborador")
    st.info("Página em construção.")

elif menu == "Ferramenta":
    st.header("Ferramenta")
    st.info("Página em construção.")

elif menu == "Relatório":
    st.header("Relatório")
    st.info("Esta página está desativada.")
