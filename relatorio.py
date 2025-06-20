import streamlit as st
import pandas as pd
import os
from datetime import datetime


def pagina_relatorio():
    st.subheader("📑 Relatório de Movimentações")

    arquivo_movimentacao = 'movimentacao.csv'
    arquivo_ferramentas = 'ferramentas.csv'

    # ========================
    # Leitura dos Arquivos
    # ========================
    if os.path.exists(arquivo_movimentacao):
        df_mov = pd.read_csv(arquivo_movimentacao, encoding='utf-8-sig')
        df_mov['DataHora'] = pd.to_datetime(df_mov['DataHora'], format='%d/%m/%Y %H:%M:%S')
    else:
        st.warning("⚠️ Nenhuma movimentação registrada ainda.")
        df_mov = pd.DataFrame()

    if os.path.exists(arquivo_ferramentas):
        df_ferramentas = pd.read_csv(arquivo_ferramentas, encoding='utf-8-sig')
    else:
        df_ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao', 'StatusConserto'])

    # ========================
    # Filtros
    # ========================
    with st.expander("🔍 Filtros"):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            matricula = st.text_input("Filtrar por Matrícula")

        with col2:
            tipo = st.selectbox("Tipo de Movimentação", ["Todos", "Retirada", "Devolução"])

        with col3:
            data_ini = st.date_input("Data Inicial")

        with col4:
            data_fim = st.date_input("Data Final")

        cod_ferramenta = st.text_input("Filtrar por Código da Ferramenta")

    df_filtrado = df_mov.copy()

    if not df_filtrado.empty:
        if matricula:
            df_filtrado = df_filtrado[df_filtrado['Matricula'].astype(str) == matricula]

        if tipo != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo]

        if data_ini:
            df_filtrado = df_filtrado[df_filtrado['DataHora'].dt.date >= data_ini]

        if data_fim:
            df_filtrado = df_filtrado[df_filtrado['DataHora'].dt.date <= data_fim]

        if cod_ferramenta:
            df_filtrado = df_filtrado[df_filtrado['CodigoFerramenta'].astype(str).str.contains(cod_ferramenta, na=False)]

    # ========================
    # Resultado
    # ========================
    st.subheader("📄 Resultado do Relatório de Movimentações")
    st.dataframe(df_filtrado)

    st.download_button(
        label="⬇️ Baixar CSV do Relatório",
        data=df_filtrado.to_csv(index=False, encoding='utf-8-sig'),
        file_name="relatorio_movimentacoes.csv",
        mime="text/csv"
    )

    # ========================
    # Resumo Geral
    # ========================
    with st.expander("📊 Resumo Geral"):
        total = len(df_filtrado)
        retiradas = len(df_filtrado[df_filtrado['Tipo'] == 'Retirada'])
        devolucoes = len(df_filtrado[df_filtrado['Tipo'] == 'Devolução'])

        st.info(f"**Total de Movimentações:** {total}")
        st.success(f"**Total de Retiradas:** {retiradas}")
        st.success(f"**Total de Devoluções:** {devolucoes}")

    # ========================
    # Ferramentas Fora (Retiradas e Não Devolvidas)
    # ========================
    with st.expander("🛠️ Ferramentas Fora (Não Devolvidas)"):
        if df_mov.empty:
            st.success("✅ Todas as ferramentas estão devolvidas.")
        else:
            status = {}

            for _, row in df_mov.iterrows():
                codigo = str(row['CodigoFerramenta'])
                status[codigo] = row['Tipo']

            retiradas = [cod for cod, tipo in status.items() if tipo == 'Retirada']

            if retiradas:
                df_retiradas = df_mov[df_mov['CodigoFerramenta'].astype(str).isin(retiradas)]
                df_ultimas = df_retiradas.sort_values('DataHora').drop_duplicates(subset=['CodigoFerramenta'], keep='last')

                df_ultimas = df_ultimas[['CodigoFerramenta', 'DescricaoFerramenta', 'DataHora', 'Nome', 'Matricula']]
                df_ultimas = df_ultimas.rename(columns={
                    'CodigoFerramenta': 'Código',
                    'DescricaoFerramenta': 'Descrição',
                    'DataHora': 'Data/Hora da Retirada',
                    'Nome': 'Com',
                    'Matricula': 'Matrícula'
                })

                st.warning(f"🔴 Total de ferramentas fora: **{len(df_ultimas)}**")
                st.dataframe(df_ultimas)

                st.download_button(
                    label="⬇️ Baixar CSV das Ferramentas Fora",
                    data=df_ultimas.to_csv(index=False, encoding='utf-8-sig'),
                    file_name="ferramentas_fora.csv",
                    mime="text/csv"
                )
            else:
                st.success("✅ Todas as ferramentas estão devolvidas.")

    # ========================
    # Ferramentas em Conserto
    # ========================
    with st.expander("🔧 Ferramentas em Conserto"):
        if df_ferramentas.empty:
            st.info("Nenhuma ferramenta cadastrada.")
        else:
            df_conserto = df_ferramentas[df_ferramentas['StatusConserto'] == 'Em Conserto']
            if df_conserto.empty:
                st.success("✅ Nenhuma ferramenta está em conserto.")
            else:
                st.warning(f"🔧 Total em conserto: {len(df_conserto)}")
                st.dataframe(df_conserto)

                st.download_button(
                    label="⬇️ Baixar CSV das Ferramentas em Conserto",
                    data=df_conserto.to_csv(index=False, encoding='utf-8-sig'),
                    file_name="ferramentas_em_conserto.csv",
                    mime="text/csv"
                )

