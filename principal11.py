import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título
st.title("Ferramentaria")

# Menu lateral
menu = st.sidebar.radio(
    "Menu",
    ["Movimentação", "Colaborador", "Ferramenta", "Relatório"]
)

if menu == "Movimentação":
    st.header("Movimentação")

    # Data e Hora atuais
    data_atual = datetime.now().strftime('%d/%m/%Y')
    hora_atual = datetime.now().strftime('%H:%M:%S')

    # Linha 1: Matrícula e Nome
    col1, col2 = st.columns(2)
    with col1:
        matricula = st.text_input("Matrícula")
    with col2:
        nome = st.text_input("Nome", value="", disabled=True)

    # Linha 2: Tipo de movimentação
    tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])

    # Linha 3: Data e Hora (somente visualização)
    col3, col4 = st.columns(2)
    with col3:
        st.text_input("Data da Movimentação", value=data_atual, disabled=True)
    with col4:
        st.text_input("Hora da Movimentação", value=hora_atual, disabled=True)

    st.markdown("---")

    st.subheader("Ferramentas")

    # Lista para armazenar as ferramentas
    ferramentas = []

    # Definir número de ferramentas que deseja adicionar
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

    # Botão Confirmar
    if st.button("Confirmar Movimentação"):
        st.success("Movimentação registrada com sucesso!")

        st.subheader("Resumo da Movimentação:")
        st.write(f"**Matrícula:** {matricula}")
        st.write(f"**Nome:** {nome}")
        st.write(f"**Tipo de Movimentação:** {tipo}")
        st.write(f"**Data:** {data_atual}")
        st.write(f"**Hora:** {hora_atual}")
        st.write(f"**Observações:** {observacoes}")

        st.write("### Ferramentas:")
        for idx, item in enumerate(ferramentas, start=1):
            st.write(f"**{idx}. {item['Ferramenta']} - {item['Descrição']}**")

# Outras páginas (em construção)
elif menu == "Colaborador":
    st.header("Colaborador")
    st.info("Página em construção.")

elif menu == "Ferramenta":
    st.header("Ferramenta")
    st.info("Página em construção.")

elif menu == "Relatório":
    st.header("Relatório")
    st.info("Página em construção.")
