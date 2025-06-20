import streamlit as st
import pandas as pd
import os


# =========================
# FUNÇÕES AUXILIARES
# =========================
arquivo_ferramentas = 'ferramentas.csv'

def carregar_ferramentas():
    if os.path.exists(arquivo_ferramentas):
        df = pd.read_csv(arquivo_ferramentas, encoding='utf-8-sig')
    else:
        df = pd.DataFrame(columns=['Codigo', 'Descricao', 'StatusConserto'])
    if 'StatusConserto' not in df.columns:
        df['StatusConserto'] = 'Disponível'
    return df


def salvar_ferramentas(df):
    df.to_csv(arquivo_ferramentas, index=False, encoding='utf-8-sig')


# =========================
# PÁGINA DE FERRAMENTAS
# =========================
def pagina_ferramenta():
    st.subheader("🛠️ Gerenciamento de Ferramentas")

    df = carregar_ferramentas()

    menu = st.radio("Escolha uma opção:", ["Cadastrar", "Editar", "Conserto", "Pesquisar"])

    # >>>>> CADASTRAR <<<<<
    if menu == "Cadastrar":
        st.subheader("➕ Cadastrar Nova Ferramenta")

        with st.form("form_cadastro"):
            codigo = st.text_input("Código da Ferramenta")
            descricao = st.text_input("Descrição")
            cadastrar = st.form_submit_button("Cadastrar")

        if cadastrar:
            if codigo and descricao:
                if codigo in df['Codigo'].astype(str).values:
                    st.warning("⚠️ Código já cadastrado!")
                else:
                    df.loc[len(df)] = [codigo, descricao, 'Disponível']
                    salvar_ferramentas(df)
                    st.success("✅ Ferramenta cadastrada com sucesso!")
            else:
                st.error("⚠️ Preencha todos os campos!")

    # >>>>> EDITAR <<<<<
    elif menu == "Editar":
        st.subheader("✏️ Editar Ferramenta")

        codigo = st.text_input("Digite o Código da Ferramenta para editar")

        if codigo:
            ferramenta = df[df['Codigo'].astype(str) == codigo]
            if not ferramenta.empty:
                index = ferramenta.index[0]
                nova_desc = st.text_input("Nova Descrição", value=ferramenta['Descricao'].values[0])

                if st.button("Salvar Alterações"):
                    df.at[index, 'Descricao'] = nova_desc
                    salvar_ferramentas(df)
                    st.success("✅ Ferramenta atualizada!")
            else:
                st.warning("⚠️ Código não encontrado!")

    # >>>>> CONSERTO <<<<<
    elif menu == "Conserto":
        st.subheader("🛠️ Gerenciar Conserto")

        codigo = st.text_input("Código da Ferramenta para Conserto")

        if codigo:
            ferramenta = df[df['Codigo'].astype(str) == codigo]
            if not ferramenta.empty:
                index = ferramenta.index[0]
                status = ferramenta['StatusConserto'].values[0]

                st.info(f"Status atual: **{status}**")

                if status == "Em Conserto":
                    if st.button("🔧 Retirar do Conserto"):
                        df.at[index, 'StatusConserto'] = "Disponível"
                        salvar_ferramentas(df)
                        st.success("✅ Ferramenta disponível novamente!")
                else:
                    if st.button("🛠️ Colocar em Conserto"):
                        df.at[index, 'StatusConserto'] = "Em Conserto"
                        salvar_ferramentas(df)
                        st.success("✅ Ferramenta marcada como em conserto!")
            else:
                st.warning("⚠️ Código não encontrado!")

    # >>>>> PESQUISAR <<<<<
    elif menu == "Pesquisar":
        st.subheader("🔍 Pesquisar Ferramenta")

        busca = st.text_input("Digite código ou nome para buscar")

        if busca:
            filtro = df[
                df['Codigo'].astype(str).str.contains(busca, na=False, case=False) |
                df['Descricao'].str.contains(busca, na=False, case=False)
            ]
            st.dataframe(filtro)
        else:
            st.dataframe(df)
