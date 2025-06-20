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
st.sidebar.title("Menu")

# Ação de cada botão do menu
if st.sidebar.button("Movimentação"):
    # Abre modal com campos de Movimentação
    with st.modal("Movimentação"):
        st.markdown("Preencha os dados abaixo:")
        matricula = st.text_input("Matrícula")
        nome = st.text_input("Nome", value="", disabled=True)
        ferramenta = st.text_input("Ferramenta")
        descricao = st.text_input("Descrição", value="", disabled=True)
        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
        if st.button("Confirmar", key="confirm_movimentacao"):
            st.success(f"Movimentação registrada: {tipo} - Matrícula: {matricula} - Ferramenta: {ferramenta}")

elif st.sidebar.button("Colaborador"):
    st.header("Colaborador")
    st.write("Você foi direcionado para o branch Colaborador.")

elif st.sidebar.button("Ferramenta"):
    st.header("Ferramenta")
    st.write("Você foi direcionado para o branch Ferramenta.")

elif st.sidebar.button("Relatorio"):
    st.header("Relatório")
    st.write("Você foi direcionado para o branch Relatório.")

else:
    st.write("Selecione uma opção no menu lateral para navegar entre os branches.")
