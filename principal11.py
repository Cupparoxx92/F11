import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título da aplicação
st.title("Ferramentaria")

# Inicializa estado de página
if 'page' not in st.session_state:
    st.session_state.page = None

# Menu lateral
st.sidebar.title("Menu")
if st.sidebar.button("Movimentação"):
    st.session_state.page = 'movimentacao'
if st.sidebar.button("Colaborador"):
    st.session_state.page = 'colaborador'
if st.sidebar.button("Ferramenta"):
    st.session_state.page = 'ferramenta'
if st.sidebar.button("Relatório"):
    st.session_state.page = 'relatorio'

# Renderiza conteúdo conforme o branch selecionado
if st.session_state.page == 'movimentacao':
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

elif st.session_state.page == 'colaborador':
    st.header("Colaborador")
    st.write("Você foi direcionado para o branch Colaborador.")

elif st.session_state.page == 'ferramenta':
    st.header("Ferramenta")
    st.write("Você foi direcionado para o branch Ferramenta.")

elif st.session_state.page == 'relatorio':
    st.header("Relatório")
    st.write("Você foi direcionado para o branch Relatório.")

else:
    st.write("Selecione uma opção no menu lateral para navegar entre os branches.")
