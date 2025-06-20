import streamlit as st
import pandas as pd
import os


# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="Cadastro de Colaboradores",
    layout="wide",
    page_icon="👥"
)

st.title("👥 Cadastro e Consulta de Colaboradores")

# =========================
# Arquivo de colaboradores
# =========================
arquivo_colaboradores = 'colaboradores.csv'
cabecalho = ['Matricula', 'Nome']

# =========================
# Inicializa o arquivo, se não existir
# =========================
if not os.path.exists(arquivo_colaboradores):
    pd.DataFrame(columns=cabecalho).to_csv(arquivo_colaboradores, index=False, encoding='utf-8-sig')

# =========================
# Carrega os dados
# =========================
df_colaboradores = pd.read_csv(arquivo_colaboradores, encoding='utf-8-sig')

# =========================
# Função para salvar colaborador
# =========================
def salvar_colaborador(matricula, nome):
    novo = pd.DataFrame({'Matricula': [matricula], 'Nome': [nome]})
    novo.to_csv(arquivo_colaboradores, mode='a', header=False, index=False, encoding='utf-8-sig')

# =========================
# CADASTRAR NOVO COLABORADOR
# =========================
st.subheader("➕ Cadastrar Novo Colaborador")

with st.form("form_cadastro"):
    col1, col2 = st.columns(2)

    with col1:
        matricula = st.text_input("Matrícula")

    with col2:
        nome = st.text_input("Nome")

    adicionar = st.form_submit_button("✅ Adicionar")

if adicionar:
    if matricula and nome:
        if matricula in df_colaboradores['Matricula'].astype(str).values:
            st.warning("⚠️ Esta matrícula já está cadastrada!")
        else:
            salvar_colaborador(matricula, nome)
            st.success(f"✅ Colaborador {nome} cadastrado com sucesso!")
            st.rerun()
    else:
        st.error("❌ Preencha todos os campos!")

# =========================
# CONSULTAR POR MATRÍCULA
# =========================
st.subheader("🔍 Consultar Nome pela Matrícula")

matricula_consulta = st.text_input("Digite a matrícula para consulta:")

if matricula_consulta:
    df_filtro = df_colaboradores[df_colaboradores['Matricula'].astype(str) == matricula_consulta]
    if not df_filtro.empty:
        nome_encontrado = df_filtro['Nome'].values[0]
        st.success(f"🔍 Nome: {nome_encontrado}")
    else:
        st.warning("⚠️ Matrícula não encontrada.")

# =========================
# Exibir todos os colaboradores cadastrados
# =========================
st.subheader("📑 Todos os Colaboradores")
st.dataframe(df_colaboradores)

st.download_button(
    label="⬇️ Baixar Lista de Colaboradores",
    data=df_colaboradores.to_csv(index=False, encoding='utf-8-sig'),
    file_name="colaboradores.csv",
    mime="text/csv"
)

