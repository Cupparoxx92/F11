import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# Fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# Dados dos arquivos
try:
    colaboradores = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()
except:
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

try:
    ferramentas = pd.read_csv('ferramentas.csv', encoding='utf-8-sig')
    ferramentas.columns = ferramentas.columns.str.strip()
    ferramentas.rename(columns={'Descrição': 'Descricao'}, inplace=True)
except:
    ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao'])

# Arquivo movimentação
mov_file = 'movimentacao.csv'
if not os.path.exists(mov_file):
    pd.DataFrame(columns=['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']).to_csv(mov_file, index=False, encoding='utf-8-sig')

# Configuração da página
st.set_page_config(page_title="Ferramentaria", layout="wide")
st.title("Ferramentaria")

menu = st.sidebar.radio("Menu", ["Movimentação", "Colaborador", "Ferramenta"])

# Controle de sessão
if 'dados_carregados' not in st.session_state:
    st.session_state.dados_carregados = False
    st.session_state.nome = ""
    st.session_state.ferramentas_preenchidas = {}

# Página Movimentação
if menu == "Movimentação":
    st.subheader("Movimentação de Ferramentas")

    with st.form("form_busca"):
        matricula = st.text_input("Matrícula")
        buscar = st.form_submit_button("🔍 Buscar Dados")

        if buscar:
            df_col = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
            if not df_col.empty:
                st.session_state.nome = df_col['Nome'].values[0]
                st.session_state.dados_carregados = True
            else:
                st.error("Matrícula não encontrada.")
                st.session_state.dados_carregados = False

    if st.session_state.dados_carregados:
        st.success(f"Colaborador: {st.session_state.nome}")

        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
        qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)

        ferramentas_selecionadas = []

        for i in range(qtd):
            with st.expander(f"Ferramenta {i+1}"):
                cod = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")

                desc = ""
                df_f = ferramentas[ferramentas['Codigo'].astype(str) == cod]
                if not df_f.empty:
                    desc = df_f['Descricao'].values[0]

                st.text_input(f"Descrição {i+1}", value=desc, disabled=True, key=f"desc{i}")

                ferramentas_selecionadas.append((cod, desc))

        observacoes = st.text_area("Observações (opcional)")

        confirmar = st.button("✅ Confirmar Movimentação")

        if confirmar:
            ferramentas_validas = [(c, d) for c, d in ferramentas_selecionadas if c and d]

            if not ferramentas_validas:
                st.error("Informe pelo menos uma ferramenta válida.")
            else:
                agora = datetime.now(fuso)
                datahora = agora.strftime('%d/%m/%Y %H:%M:%S')
                tools_str = "; ".join(f"{c} - {d}" for c, d in ferramentas_validas)

                row = [datahora, matricula, st.session_state.nome, tipo, tools_str, observacoes]

                with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)

                st.success("Movimentação registrada com sucesso!")

                # Gerar resumo
                resumo = f"""
============================================
            RESUMO DE MOVIMENTAÇÃO
============================================
Data/Hora: {datahora}
Nome: {st.session_state.nome}
Matrícula: {matricula}
Tipo: {tipo}

Ferramentas:
"""
                for c, d in ferramentas_validas:
                    resumo += f" - {c} - {d}\n"

                resumo += f"""
Observações: {observacoes}

Assinatura: ____________________________________________

============================================
                """

                st.download_button(
                    label="📄 Baixar Resumo para Impressão",
                    data=resumo,
                    file_name=f"resumo_{matricula}_{agora.strftime('%Y%m%d%H%M%S')}.txt",
                    mime="text/plain"
                )
