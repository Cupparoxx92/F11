import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"  # Garante que o menu lateral fique sempre visível
)

# Título da aplicação
st.title("Ferramentaria")

# Inicializa estado de página
if 'page' not in st.session_state:
    st.session_state.page = None

# Menu lateral
st.sidebar.title("Menu")

# Botões do menu definem o branch a ser exibido
if st.sidebar.button("Movimentação"):
    st.session_state.page = 'movimentacao'
if st.sidebar.button("Colaborador"):
    st.session_state.page = 'colaborador'
if st.sidebar.button("Ferramenta"):
    st.session_state.page = 'ferramenta'
if st.sidebar.button("Relatorio"):
    st.session_state.page = 'relatorio'

# Roteamento para cada branch
if st.session_state.page == 'movimentacao':
    st.header("Movimentação")
    st.write("Você foi direcionado para o branch Movimentação.")
elif st.session_state.page == 'colaborador':
    st.header("Colaborador")
    st.write("Você foi direcionado para o branch Colaborador.")
elif st.session_state.page == 'ferramenta':
    st.header("Ferramenta")
    st.write("Você foi direcionado para o branch Ferramenta.")
elif st.session_state.page == 'relatorio':
    st.header("Relatorio")
    st.write("Você foi direcionado para o branch Relatorio.")
else:
    st.write("Selecione uma opção no menu lateral para navegar entre os branches.")
