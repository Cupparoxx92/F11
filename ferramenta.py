import streamlit as st
import pandas as pd
import os


# =========================
# ARQUIVO DE FERRAMENTAS
# =========================
arquivo_ferramentas = 'ferramentas.csv'
cabecalho = ['Codigo', 'Descricao', 'Status']  # Status pode ser 'Disponível' ou 'Em Conserto'


# =========================
# FUNÇÕES AUXILIARES
# =========================
def carregar_ferramentas():
    if os.path.exists(arquivo_ferramentas):
        df = pd.read_csv(arquivo_ferramentas, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
    else:
        df = pd.DataFrame(columns=cabecalho)
    return df


def salvar_ferramentas(df):
    df.to_csv(arquivo_ferramentas, index=False, encoding='utf-8-sig')


# =========================
# PÁGINA DE FERRAMENTAS
# =========================
def pagina_ferramenta():
    st.subheader("🛠️ Gerenciamento de Ferramentas")

    df = carregar_ferramentas()

    # ------------------------------
    # Bloco 1 - Cadastro de Ferramentas
    # ------------------------------
    st.markdown("### ➕ Cadastrar Nova Ferramenta")
    with st.form("cadastro_ferramenta"):
        col1, col2 = st.columns(2)
        with col1:
            codigo = st.text_input("Código da Ferramenta")
        with col2:
            descricao = st.text_input("Descrição da Ferramenta")

        cadastrar = st.form_submit_button("✅ Cadastrar")

        if cadastrar:
            if codigo and descricao:
                if codigo in df['Codigo'].astype(str).values:
                    st.warning("⚠️ Código já cadastrado!")
                else:
                    novo = pd.DataFrame([[codigo, descricao, 'Disponível']], columns=cabecalho)
                    df = pd.concat([df, novo], ignore_index=True)
                    salvar_ferramentas(df)
                    st.success("✅ Ferramenta cadastrada com sucesso!")
            else:
                st.warning("⚠️ Preencha todos os campos.")

    # ------------------------------
    # Bloco 2 - Edição e Exclusão
    # ------------------------------
    st.markdown("### ✏️ Editar ou 🗑️ Excluir Ferramenta")
    busca = st.text_input("🔍 Buscar por Código ou Descrição")

    filtro = df[df['Codigo'].astype(str).str.contains(busca, na=False) | df['Descricao'].str.contains(busca, na=False)]

    st.dataframe(filtro)

    if not filtro.empty:
        cod_editar = st.selectbox("Selecione o Código da Ferramenta para editar ou excluir", filtro['Codigo'].tolist())

        ferramenta = df[df['Codigo'].astype(str) == str(cod_editar)]
        if not ferramenta.empty:
            nova_desc = st.text_input("Editar Descrição", ferramenta['Descricao'].values[0])
            novo_status = st.selectbox("Status", ['Disponível', 'Em Conserto'], index=0 if ferramenta['Status'].values[0] == 'Disponível' else 1)

            col1, col2 = st.columns(2)
            editar = col1.button("💾 Salvar Alterações")
            excluir = col2.button("🗑️ Excluir Ferramenta")

            if editar:
                df.loc[df['Codigo'].astype(str) == str(cod_editar), 'Descricao'] = nova_desc
                df.loc[df['Codigo'].astype(str) == str(cod_editar), 'Status'] = novo_status
                salvar_ferramentas(df)
                st.success("✅ Alterações salvas com sucesso!")

            if excluir:
                df = df[df['Codigo'].astype(str) != str(cod_editar)]
                salvar_ferramentas(df)
                st.success("🗑️ Ferramenta excluída com sucesso!")

    # ------------------------------
    # Bloco 3 - Relatório Completo
    # ------------------------------
    st.markdown("### 📋 Relatório Completo de Ferramentas")
    st.dataframe(df)

    st.download_button(
        label="⬇️ Baixar CSV de Ferramentas",
        data=df.to_csv(index=False, encoding='utf-8-sig'),
        file_name="relatorio_ferramentas.csv",
        mime="text/csv"
    )

