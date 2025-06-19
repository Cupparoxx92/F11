import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"  # Garante que o menu lateral fique sempre visível
)

# Título da aplicação
st.title("Ferramentaria")

# Menu lateral
st.sidebar.title("Menu")

# Botões do menu
if st.sidebar.button("Movimentação"):
    st.write("Você selecionou: Movimentação")

if st.sidebar.button("Colaborador"):
    st.write("Você selecionou: Colaborador")

if st.sidebar.button("Ferramenta"):
    st.write("Você selecionou: Ferramenta")

if st.sidebar.button("Relatorio"):
    st.write("Você selecionou: Relatorio")

# Conteúdo principal pode ser adicionado abaixo
# Exemplo:
# st.write("Bem-vindo à Ferramentaria! Selecione uma opção no menu lateral.")

