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

# Variável de controle no session_state
if 'gerar_resumo' not in st.session_state:
    st.session_state.gerar_resumo = False
    st.session_state.resumo_arquivo = ""
    st.session_state.matricula_atual = ""

# MOVIMENTAÇÃO
if menu == "Movimentação":
    st.header("Movimentação")

    with st.form("form_mov"):
        matricula = st.text_input("Matrícula")
        nome = ""
        if matricula:
            df_col = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
            if not df_col.empty:
                nome = df_col['Nome'].values[0]
        st.text_input("Nome", value=nome, disabled=True)

        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
        qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)

        selecionadas = []
        for i in range(qtd):
            with st.expander(f"Ferramenta {i+1}"):
                codigo = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")
                desc = ""
                if codigo:
                    df_f = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                    if not df_f.empty:
                        desc = df_f['Descricao'].values[0]
                st.text_input(f"Descrição {i+1}", value=desc, disabled=True, key=f"desc{i}")
                selecionadas.append((codigo, desc))

        observacoes = st.text_area("Observações (opcional)")

        submit = st.form_submit_button("Confirmar Movimentação")

        if submit:
            if not nome:
                st.error("Informe uma matrícula válida antes de registrar.")
            else:
                valid = [(c, d) for c, d in selecionadas if c and d]
                if not valid:
                    st.error("Informe pelo menos uma ferramenta válida antes de registrar.")
                else:
                    agora = datetime.now(fuso)
                    datahora = agora.strftime('%d/%m/%Y %H:%M:%S')
                    tools_str = "; ".join(f"{c} - {d}" for c, d in valid)

                    row = [datahora, matricula, nome, tipo, tools_str, observacoes]

                    # Registrar no CSV
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
Nome: {nome}
Matrícula: {matricula}
Tipo: {tipo}

Ferramentas:
"""
                    for c, d in valid:
                        resumo += f" - {c} - {d}\n"

                    resumo += f"""
Observações: {observacoes}

Assinatura: ____________________________________________

============================================
                    """

                    st.session_state.gerar_resumo = True
                    st.session_state.resumo_arquivo = resumo
                    st.session_state.matricula_atual = matricula

# Download aparece apenas após confirmar
if st.session_state.get('gerar_resumo'):
    st.download_button(
        label="📄 Baixar Resumo para Impressão",
        data=st.session_state.resumo_arquivo,
        file_name=f"resumo_{st.session_state.matricula_atual}_{datetime.now(fuso).strftime('%Y%m%d%H%M%S')}.txt",
        mime="text/plain"
    )

