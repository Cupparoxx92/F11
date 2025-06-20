import streamlit as st
import pandas as pd
import os
from datetime import datetime


def pagina_relatorio():
    st.subheader("📑 Relatório de Movimentações")

    arquivo_movimentacao = 'movimentacao.csv'

    if not os.path.exists(arquivo_movimentacao):
        st.warning("⚠️ Nenhuma movimentação registrada ainda.")
        return

    try:
        df_mov = pd.read_csv(arquivo_movimentacao, encoding='utf-8-sig')
        df_mov['DataHora'] = pd.to_datetime(df_mov['DataHora'], format='%d/%m/%Y %H:%M:%S')

        # ------------------------------
        # Bloco de Filtros
        # ------------------------------
        with st.expander("🔍 Filtros"):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                matricula_filtro = st.text_input("Filtrar por Matrícula")

            with col2:
                tipo_filtro = st.selectbox("Tipo", ["Todos", "Retirada", "Devolução"])

            with col3:
                data_ini = st.date_input("Data Inicial")

            with col4:
                data_fim = st.date_input("Data Final")

            codigo_ferramenta = st.text_input("Filtrar por Código da Ferramenta")

        df_filtrado = df_mov.copy()

        if matricula_filtro:
            df_filtrado = df_filtrado[df_filtrado['Matricula'].astype(str) == matricula_filtro]

        if tipo_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo_filtro]

        if data_ini:
            df_filtrado = df_filtrado[df_filtrado['DataHora'].dt.date >= data_ini]

        if data_fim:
            df_filtrado = df_filtrado[df_filtrado['DataHora'].dt.date <= data_fim]

        if codigo_ferramenta:
            df_filtrado = df_filtrado[df_filtrado['CodigoFerramenta'].astype(str).str.contains(codigo_ferramenta)]

        # ------------------------------
        # Resultado do Relatório
        # ------------------------------
        st.subheader("📄 Resultado do Relatório")
        st.dataframe(df_filtrado)

        st.download_button(
            label="⬇️ Baixar CSV do Relatório",
            data=df_filtrado.to_csv(index=False, encoding='utf-8-sig'),
            file_name="relatorio_movimentacoes.csv",
            mime="text/csv"
        )

        # ------------------------------
        # Resumo Geral
        # ------------------------------
        with st.expander("📊 Resumo Geral"):
            total_mov = len(df_filtrado)
            total_retiradas = len(df_filtrado[df_filtrado['Tipo'] == 'Retirada'])
            total_devolucoes = len(df_filtrado[df_filtrado['Tipo'] == 'Devolução'])

            st.success(f"**Total de Movimentações:** {total_mov}")
            st.info(f"**Total de Retiradas:** {total_retiradas}")
            st.info(f"**Total de Devoluções:** {total_devolucoes}")

        # ------------------------------
        # Ferramentas Atualmente Fora
        # ------------------------------
        with st.expander("🛠️ Ferramentas Atualmente Fora (Não Devolvidas)"):
            df_ret = df_mov.copy()
            ferramentas_status = {}

            for _, row in df_ret.iterrows():
                codigo = str(row['CodigoFerramenta'])
                if codigo:
                    ferramentas_status[codigo] = {
                        'Status': row['Tipo'],
                        'DataHora': row['DataHora'],
                        'Matricula': row['Matricula'],
                        'Nome': row['Nome'],
                        'Descricao': row['DescricaoFerramenta']
                    }

            retiradas = {
                k: v for k, v in ferramentas_status.items() if v['Status'] == 'Retirada'
            }

            if retiradas:
                st.warning(f"🔴 Total de ferramentas fora: **{len(retiradas)}**")

                df_exibicao = pd.DataFrame([
                    {
                        'Código': cod,
                        'Descrição': v['Descricao'],
                        'Data/Hora da Retirada': v['DataHora'],
                        'Com': f"{v['Nome']} (Matrícula: {v['Matricula']})"
                    }
                    for cod, v in retiradas.items()
                ])

                st.dataframe(df_exibicao)

                st.download_button(
                    label="⬇️ Baixar CSV das Ferramentas Fora",
                    data=df_exibicao.to_csv(index=False, encoding='utf-8-sig'),
                    file_name="ferramentas_fora.csv",
                    mime="text/csv"
                )
            else:
                st.success("✅ Todas as ferramentas estão devolvidas.")

    except Exception as e:
        st.warning("⚠️ Erro ao carregar os dados.")
        st.error(e)
