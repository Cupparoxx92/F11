import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# Fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# ============================== Carregar dados ==============================

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
header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
if not os.path.exists(mov_file):
    pd.DataFrame(columns=header).to_csv(mov_file, index=False, encoding='utf-8-sig')

# ============================== Configurar página ==============================

st.set_page_config(
    page_title="Controle de Ferramentas",
    layout="wide"
)

st.title("📦 Registrar Movimentação")

# ============================== FORMULÁRIO ==============================

with st.form("form_mov"):

    col1, col2 = st.columns([2, 1])
    with col1:
        matricula = st.text_input("Matrícula")
    with col2:
        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])

    nome = ""
    if matricula:
        busca = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
        if not busca.empty:
            nome = busca['Nome'].values[0]

    st.text_input("Nome", value=nome, disabled=True)

    qtd = st.number_input("Quantidade de Ferramentas", min_value=1, step=1, value=1)

    ferramentas_selecionadas = []
    for i in range(qtd):
        with st.expander(f"Ferramenta {i+1}"):
            codigo = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")
            descricao = ""
            if codigo:
                busca = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                if not busca.empty:
                    descricao = busca['Descricao'].values[0]
            st.text_input(f"Descrição {i+1}", value=descricao, disabled=True, key=f"desc{i}")
            ferramentas_selecionadas.append((codigo, descricao))

    observacoes = st.text_area("Observações (opcional)")

    # ✅ Botão dentro do form
    confirmar = st.form_submit_button("✅ Confirmar Movimentação")

# ============================== Botão LIMPAR fora do form ==============================

if st.button("🧹 Limpar"):
    st.experimental_rerun()

# ============================== AÇÃO DO BOTÃO CONFIRMAR ==============================

if confirmar:

    if not nome:
        st.error("⚠️ Informe uma matrícula válida antes de continuar.")
    else:
        ferramentas_validas = [(c, d) for c, d in ferramentas_selecionadas if c and d]
        if not ferramentas_validas:
            st.error("⚠️ Informe pelo menos uma ferramenta válida antes de registrar.")
        else:
            agora = datetime.now(fuso)
            datahora = agora.strftime('%d/%m/%Y %H:%M:%S')

            ferramentas_txt = "; ".join(f"{c} - {d}" for c, d in ferramentas_validas)

            registro = [datahora, matricula, nome, tipo, ferramentas_txt, observacoes]

            with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(registro)

            st.success("✅ Movimentação registrada com sucesso!")

            # 📄 Gerar resumo para impressão
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
