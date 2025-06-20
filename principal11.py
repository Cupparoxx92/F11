import streamlit as st
from datetime import datetime
import pandas as pd
import pytz

# Fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# === Carrega bases ===
colaboradores = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
colaboradores.columns = colaboradores.columns.str.strip()

ferramentas = pd.read_csv('ferramentas.csv', encoding='utf-8-sig')
ferramentas.columns = ferramentas.columns.str.strip()
# renomeia a coluna acentuada
ferramentas.rename(columns={'Descrição':'Descricao'}, inplace=True)

# === Streamlit setup ===
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Ferramentaria")
menu = st.sidebar.radio("Menu",
    ["Movimentação", "Colaborador", "Ferramenta", "Relatório"]
)

if menu == "Movimentação":
    st.header("Movimentação")

    # Matrícula → Nome
    col1, col2 = st.columns(2)
    with col1:
        matricula = st.text_input("Matrícula")
    with col2:
        nome = ""
        if matricula:
            res = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
            nome = res['Nome'].values[0] if not res.empty else "Matrícula não encontrada"
        st.text_input("Nome", value=nome, disabled=True)

    tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
    st.markdown("---")
    st.subheader("Ferramentas")

    selecionadas = []
    qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)
    for i in range(qtd):
        with st.expander(f"Ferramenta {i+1}"):
            c1, c2 = st.columns(2)
            with c1:
                codigo = st.text_input(f"Código {i+1}", key=f"cod_{i}")
            with c2:
                descricao = ""
                if codigo:
                    res = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                    descricao = res['Descricao'].values[0] if not res.empty else "Código não encontrado"
                st.text_input(f"Descrição {i+1}", value=descricao, disabled=True)
            selecionadas.append((codigo, descricao))

    st.markdown("---")
    obs = st.text_area("Observações (opcional)")

    if st.button("Confirmar Movimentação"):
        agora = datetime.now(fuso)
        st.success("Movimentação registrada!")
        st.write(f"**Data/Hora:** {agora.strftime('%d/%m/%Y %H:%M:%S')}")
        st.write(f"**Matrícula:** {matricula} — **Nome:** {nome}")
        st.write(f"**Tipo:** {tipo}")
        st.write("**Ferramentas:**")
        for idx,(c,d) in enumerate(selecionadas,1):
            st.write(f"{idx}. {c} ― {d}")
        st.write(f"**Observações:** {obs}")

# placeholders...
elif menu == "Colaborador":
    st.header("Colaborador"); st.info("Em construção.")
elif menu == "Ferramenta":
    st.header("Ferramenta"); st.info("Em construção.")
elif menu == "Relatório":
    st.header("Relatório"); st.info("Em construção.")
