import streamlit as st
import pandas as pd
import os


def pagina_colaborador():
    st.subheader("👥 Gerenciamento de Colaboradores")

    arquivo_colaboradores = 'colaboradores.csv'

    if not os.path.exists(arquivo_colaboradores):
        pd.DataFrame(columns=['Matricula', 'Nome']).to_csv(arquivo_colaboradores, index=False, encoding='utf-8-sig')

    df_colab = pd.read_csv(arquivo_colaboradores, encoding='utf-8-sig')

    aba = st.radio("Selecione a opção:", ["➕ Cadastrar Colaborador", "🔍 Consultar Colaborador"])

    if aba == "➕ Cadastrar Colaborador":
        with st.form("form_cadastro"):
            st.subheader("➕ Cadastrar Novo Colaborador")
            matricula = st.text_input("Matrícula")
            nome = st.text_input("Nome do Colaborador")

            cadastrar = st.form_submit_button("Salvar")

            if cadastrar:
                if matricula and nome:
                    if matricula in df_colab['Matricula'].astype(str).values:
                        st.error("⚠️ Matrícula já cadastrada.")
                    else:
                        novo = pd.DataFrame({'Matricula': [matricula], 'Nome': [nome]})
                        df_colab = pd.concat([df_colab, novo], ignore_index=True)
                        df_colab.to_csv(arquivo_colaboradores, index=False, encoding='utf-8-sig')
                        st.success("✅ Colaborador cadastrado com sucesso!")
                else:
                    st.warning("⚠️ Preencha todos os campos.")

    if aba == "🔍 Consultar Colaborador":
        st.subheader("🔍 Consultar por Matrícula ou Nome")
        busca = st.text_input("Digite a matrícula ou nome para consultar").strip()

        if busca:
            resultado = df_colab[
                (df_colab['Matricula'].astype(str).str.contains(busca, case=False)) |
                (df_colab['Nome'].str.contains(busca, case=False, na=False))
            ]

            if not resultado.empty:
                for idx, row in resultado.iterrows():
                    st.info(f"👤 Matrícula: **{row['Matricula']}**\n\n📛 Nome: **{row['Nome']}**")
            else:
                st.warning("⚠️ Nenhum colaborador encontrado com essa matrícula ou nome.")

