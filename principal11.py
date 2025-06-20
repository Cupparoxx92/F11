import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os
import csv

# =========================
# Configurações Iniciais
# =========================
st.set_page_config(
    page_title="Controle de Ferramentas",
    layout="wide",
    page_icon="🔧"
)

st.title("🔧 Registrar Movimentação")

# Fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# =========================
# Carregar os Dados
# =========================
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

# Arquivo de movimentações
mov_file = 'movimentacao.csv'
mov_header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']

if not os.path.exists(mov_file):
    pd.DataFrame(columns=mov_header).to_csv(mov_file, index=False, encoding='utf-8-sig')

# =========================
# Formulário
# =========================
with st.form("formulario"):

    col1, col2 = st.columns(2)

    with col1:
        matricula = st.text_input("Matrícula")
        nome = ""
        if matricula:
            df_col = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
            if not df_col.empty:
                nome = df_col['Nome'].values[0]
        st.text_input("Nome", value=nome, disabled=True)

    with col2:
        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
        qtd = st.number_input("Quantidade de Ferramentas", min_value=1, step=1, value=1)

    selecionadas = []
    for i in range(qtd):
        with st.expander(f"Ferramenta {i + 1}"):
            codigo = st.text_input(f"Código da Ferramenta {i + 1}", key=f"cod_{i}")
            desc = ""
            if codigo:
                df_ferr = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                if not df_ferr.empty:
                    desc = df_ferr['Descricao'].values[0]
            st.text_input(f"Descrição {i + 1}", value=desc, disabled=True, key=f"desc_{i}")
            selecionadas.append((codigo, desc))

    observacoes = st.text_area("Observações (opcional)")

    col3, col4 = st.columns([1, 5])
    submit = col3.form_submit_button("✅ Confirmar Movimentação")
    limpar = col4.form_submit_button("🧹 Limpar")

# =========================
# Processamento
# =========================
if limpar:
    st.rerun()

if submit:
    if not nome:
        st.error("⚠️ Informe uma matrícula válida antes de registrar.")
    else:
        ferramentas_validas = [(c, d) for c, d in selecionadas if c and d]
        if not ferramentas_validas:
            st.error("⚠️ Informe pelo menos uma ferramenta válida antes de registrar.")
        else:
            agora = datetime.now(fuso).strftime('%d/%m/%Y %H:%M:%S')
            ferramentas_str = "; ".join([f"{c} - {d}" for c, d in ferramentas_validas])

            nova_mov = [agora, matricula, nome, tipo, ferramentas_str, observacoes]

            with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(nova_mov)

            st.success("✅ Movimentação registrada com sucesso!")

            # Gerar resumo para impressão
            resumo = f"""
            =============================================
                       RESUMO DE MOVIMENTAÇÃO
            =============================================
            Data/Hora: {agora}
            Nome: {nome}
            Matrícula: {matricula}
            Tipo de Movimentação: {tipo}

            Ferramentas:
            """

            for c, d in ferramentas_validas:
                resumo += f" - {c} - {d}\n"

            resumo += f"""
            \nObservações: {observacoes}
            \n\nAssinatura: _______________________________________
            =============================================
            """

            # Download do resumo
            st.download_button(
                label="📄 Baixar Resumo para Impressão",
                data=resumo,
                file_name=f"resumo_{matricula}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt",
                mime="text/plain"
            )
