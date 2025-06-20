import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título da aplicação
st.title("Ferramentaria")

# Menu lateral
menu = st.sidebar.radio(
    "Menu",
    ["Movimentação", "Colaborador", "Ferramenta", "Relatório"]
)

# Página Movimentação
if menu == "Movimentação":
    st.header("Movimentação")

    # Linha 1: Matrícula e Nome
    col1, col2 = st.columns(2)
    with col1:
        matricula = st.text_input("Matrícula")
    with col2:
        nome = st.text_input("Nome", value="", disabled=True)

    # Linha 2: Ferramenta e Descrição
    col3, col4 = st.columns(2)
    with col3:
        ferramenta = st.text_input("Ferramenta")
    with col4:
        descricao = st.text_input("Descrição", value="", disabled=True)

    # Linha 3: Tipo de movimentação
    tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])

    # Botão confirmar
    if st.button("Confirmar Movimentação"):
        st.success(
            f"Movimentação registrada com sucesso!\n"
            f"Matrícula: {matricula} | Ferramenta: {ferramenta} | Tipo: {tipo}"
        )

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