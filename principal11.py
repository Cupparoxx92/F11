import streamlit as st
from datetime import datetime
import pandas as pd
import pytz

# Definir o fuso horário para horário local (ex.: Brasil)
fuso = pytz.timezone('America/Sao_Paulo')

# =======================
# Carregar base de colaboradores
# =======================
try:
    colaboradores = pd.read_csv('colaboradores.csv', encoding='latin1')  # ou utf-8-sig
except Exception as e:
    st.error(f"Erro ao carregar o arquivo de colaboradores: {e}")
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

# =======================
# Configuração da página
# =======================
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================
# Título e Menu
# =======================
st.title("Ferramentaria")

menu = st.sidebar.radio(
    "Menu",
    ["Movimentação", "Colaborador", "Ferramenta", "Relatório"]
)

# =======================
# Página Movimentação
# =======================
if menu == "Movimentação":
    st.header("Movimentação")

    # Linha 1: Matrícula e Nome
    col1, col2 = st.columns(2)
    with col1:
        matricula = st.text_input("Matrícula")
    with col2:
        nome = ""
        if matricula:
            resultado = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
            if not resultado.empty:
                nome = resultado['Nome'].values[0]
            else:
                nome = "Matrícula não encontrada"
        st.text_input("Nome", value=nome, disabled=True)

    # Linha 2: Tipo de movimentação
    tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])

    st.markdown("---")

    st.subheader("Ferramentas")

    # Lista para armazenar as ferramentas
    ferramentas = []

    # Quantidade de ferramentas
    qtd_ferramentas = st.number_input(
        "Quantidade de Ferramentas", min_value=1, step=1, value=1
    )

    for i in range(qtd_ferramentas):
        with st.expander(f"Ferramenta {i + 1}"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                ferramenta = st.text_input(f"Nome da Ferramenta {i + 1}", key=f"ferramenta_{i}")
            with col_f2:
                descricao = st.text_input(f"Descrição {i + 1}", key=f"descricao_{i}")

            ferramentas.append({"Ferramenta": ferramenta, "Descrição": descricao})

    st.markdown("---")

    # Observações
    observacoes = st.text_area("Observações (opcional)")

    # =======================
    # Botão Confirma

