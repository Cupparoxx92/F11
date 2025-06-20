import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# Configurar fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# ⬇️ Carregar dados dos colaboradores
try:
    colaboradores = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()
except:
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

# ⬇️ Carregar dados das ferramentas
try:
    ferramentas = pd.read_csv('ferramentas.csv', encoding='utf-8-sig')
    ferramentas.columns = ferramentas.columns.str.strip()
    ferramentas.rename(columns={'Descrição': 'Descricao'}, inplace=True)
except:
    ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao'])

# ⬇️ Arquivo de movimentações
mov_file = 'movimentacao.csv'
mov_header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
if not os.path.exists(mov_file):
    pd.DataFrame(columns=mov_header).to_csv(mov_file, index=False, encoding='utf-8-sig')

# ⬇️ Configuração da página
st.set_page_config(
    page_title="Controle de Movimentação de Ferramentas",
    layout="wide",
)

st.title("📦 Registrar Movimentação")

# ========================= FORMULÁRIO =========================
with st.form("form_mov"):

    col1, col2 = st.columns([2, 1])
    with col1:
        matricula = st.text_input("Matrícula", key="matricula")
    with col2:
        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])

    nome = ""
    if matricula:
        df_col = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
        if not df_col.empty:
            nome = df_col['Nome'].values[0]
    st.text_input("Nome", value=nome, disabled=True)

    qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)

    selecionadas = []
    for i in range(qtd):
        with st.expander(f"Ferramenta {i+1}"):
            codigo = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")
            desc = ""
            if codigo:
                df_f = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                if not df_f.empty:
                    desc = df_f['Descricao']._
