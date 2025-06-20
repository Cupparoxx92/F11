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
if st.sidebar.button("Relatorio"):
    st.session_state.page = 'relatorio'

# Renderiza conteúdo conforme o branch selecionado
if st.session_state.page == 'movimentacao':
    st.header("Movimentação")
    # Campos de movimentação
    matricula = st.text_input("Matrícula")
    nome = st.text_input("Nome", value="", disabled=True)
    ferramenta = st.text_input("Ferramenta")
    descricao = st.text_input("Descrição", value="", disabled=True)
    tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
    if st.button("Confirmar Movimentação", key="confirm_movimentacao"):
        st.success(f"Movimentação registrada: {tipo} - Matrícula: {matricula} - Ferramenta: {ferramenta}")

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
