import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# ——————————————————————————————————————————————————————————————
# Configurações iniciais
st.set_page_config(page_title="Controle de Ferramentas", layout="wide")
st.title("🔧 Controle de Movimentação de Ferramentas")

fuso = pytz.timezone('America/Sao_Paulo')

# Carregar dados
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

# Garantir arquivo de movimentações
mov_file = 'movimentacao.csv'
header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
if not os.path.exists(mov_file):
    pd.DataFrame(columns=header).to_csv(mov_file, index=False, encoding='utf-8-sig')

# ——————————————————————————————————————————————————————————————
# Interface

st.subheader("🔄 Registrar Movimentação")

with st.form("form_mov"):
    col1, col2 = st.columns([3, 1])

    with col1:
        matricula = st.text_input("Matrícula")
        nome = ""
        if matricula:
            df_colab = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
            if not df_colab.empty:
                nome = df_colab['Nome'].values[0]
        st.text_input("Nome", value=nome, disabled=True)

    with col2:
        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
        qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)

    ferramentas_selecionadas = []
    for i in range(qtd):
        with st.expander(f"Ferramenta {i+1}"):
            codigo = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")
            descricao = ""
            if codigo:
                df_ferr = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                if not df_ferr.empty:
                    descricao = df_ferr['Descricao'].values[0]
            st.text_input(f"Descrição {i+1}", value=descricao, disabled=True, key=f"desc{i}")
            ferramentas_selecionadas.append((codigo, descricao))

    observacoes = st.text_area("Observações (opcional)")

    col_confirma, col_limpa = st.columns([1, 1])
    confirmar = col_confirma.form_submit_button("✅ Confirmar Movimentação")
    limpar = col_limpa.form_submit_button("🧹 Limpar")

# ——————————————————————————————————————————————————————————————
# Funções dos botões

if limpar:
    st.rerun()

if confirmar:
    if not nome:
        st.error("⚠️ Matrícula inválida. Verifique.")
    else:
        ferramentas_validas = [(c, d) for c, d in ferramentas_selecionadas if c and d]
        if not ferramentas_validas:
            st.error("⚠️ Informe pelo menos uma ferramenta válida antes de registrar.")
        else:
            datahora = datetime.now(fuso).strftime('%d/%m/%Y %H:%M:%S')
            ferramentas_str = "; ".join(f"{c} - {d}" for c, d in ferramentas_validas)

            nova_linha = [datahora, matricula, nome, tipo, ferramentas_str, observacoes]

            with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(nova_linha)

            st.success("✅ Movimentação registrada com sucesso!")

            resumo = f"""
=================================================================
                  RESUMO DE MOVIMENTAÇÃO
=================================================================
Data/Hora: {datahora}
Nome: {nome}
Matrícula: {matricula}
Tipo: {tipo}

Ferramentas:
"""
            for c, d in ferramentas_validas:
                resumo += f" - {c} - {d}\n"

            resumo += f"""
Observações: {observacoes}

Assinatura: _______________________________________________

=================================================================
"""

            st.download_button(
                label="📄 Baixar Resumo para Impressão",
                data=resumo,
                file_name=f"resumo_{matricula}_{datetime.now(fuso).strftime('%Y%m%d%H%M%S')}.txt",
                mime="text/plain"
            )
