import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"  # Garante que o menu lateral fique sempre visível
)

# Título da aplicação
st.title("Ferramentaria")

# Menu lateral como seleção única para navegação
menu = st.sidebar.radio(
    "Menu",
    ["Movimentação", "Colaborador", "Ferramenta", "Relatorio"]
)

# Lógica de roteamento entre páginas
if menu == "Movimentação":
    st.header("Movimentação")
    # Aqui você implementa o conteúdo específico da página Movimentação
    st.write("Você está na página de Movimentação.")
elif menu == "Colaborador":
    st.header("Colaborador")
    # Conteúdo página Colaborador
    st.write("Você está na página de Colaborador.")
elif menu == "Ferramenta":
    st.header("Ferramenta")
    # Conteúdo página Ferramenta
    st.write("Você está na página de Ferramenta.")
else:  # Relatorio
    st.header("Relatorio")
    # Conteúdo página Relatorio
    st.write("Você está na página de Relatorio.")

