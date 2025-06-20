import streamlit as st
from datetime import datetime
import pandas as pd
import pytz

# Configura fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# Carrega as bases
try:
    colaboradores = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()

    ferramentas = pd.read_csv('ferramentas.csv', encoding='utf-8-sig')
    ferramentas.columns = ferramentas.columns.str.strip()
except Exception as e:
    st.error(f"Erro ao carregar os arquivos: {e}")
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])
    ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao'])

# Configuração da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e menu lateral
st.title("Ferramentaria")
menu = st.sidebar.radio(
    "Menu",
    ["Movimentação", "Colaborador", "Ferramenta", "Relatório"]
)

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

    ferramentas_selecionadas = []

    qtd_ferramentas = st.number_input(
        "Quantidade de Ferramentas", min_value=1, step=1, value=1
    )

    for i in range(qtd_ferramentas):
        with st.expander(f"Ferramenta {i + 1}"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                codigo = st.text_input(f"Código da Ferramenta {i + 1}", key=f"codigo_{i}")
            with col_f2:
                descricao = ""
                if codigo:
                    resultado = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                    if not resultado.empty:
                        descricao = resultado['Descricao'].values[0]
                    else:
                        descricao = "Código não encontrado"
                st.text_input(f"Descrição {i + 1}", value=descricao, disabled=True)

            ferramentas_selecionadas.append({"Codigo": codigo, "Descricao": descricao})

    st.markdown("---")
    observacoes = st.text_area("Observações (opcional)")

    if st.button("Confirmar Movimentação"):
        agora = datetime.now(fuso)
        data_atual = agora.strftime('%d/%m/%Y')
        hora_atual = agora.strftime('%H:%M:%S')

        st.success("Movimentação registrada com sucesso!")

        st.subheader("Resumo da Movimentação:")
        st.write(f"**Matrícula:** {matricula}")
        st.write(f"**Nome:** {nome}")
        st.write(f"**Tipo de Movimentação:** {tipo}")
        st.write(f"**Data:** {data_atual}")
        st.write(f"**Hora:** {hora_atual}")
        st.write(f"**Observações:** {observacoes}")

        st.write("### Ferramentas:")
        for idx, item in enumerate(ferramentas_selecionadas, start=1):
            st.write(f"**{idx}. {item['Codigo']} - {item['Descricao']}**")

# Outras páginas (placeholders)
elif menu == "Colaborador":
    st.header("Colaborador")
    st.info("Página em construção.")

elif menu == "Ferramenta":
    st.header("Ferramenta")
    st.info("Página em construção.")

elif menu == "Relatório":
    st.header("Relatório")
    st.info("Página em construção.")
