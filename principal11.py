import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# ——————————————————————————————————————————————————————————————
# Fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# Carregar colaboradores
try:
    colaboradores = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()
except:
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

# Carregar ferramentas
try:
    ferramentas = pd.read_csv('ferramentas.csv', encoding='utf-8-sig')
    ferramentas.columns = ferramentas.columns.str.strip()
    ferramentas.rename(columns={'Descrição': 'Descricao'}, inplace=True)
except:
    ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao'])

# Arquivo de movimentação
mov_file = 'movimentacao.csv'
cabecalho = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
if not os.path.exists(mov_file):
    pd.DataFrame(columns=cabecalho).to_csv(mov_file, index=False, encoding='utf-8-sig')

# ——————————————————————————————————————————————————————————————
# Configuração da página
st.set_page_config(
    page_title="Controle de Ferramentas",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔧 Controle de Movimentação de Ferramentas")

# Estado do formulário
if 'registrado' not in st.session_state:
    st.session_state['registrado'] = False

# Formulário
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
        qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)

    ferramentas_selecionadas = []

    for i in range(qtd):
        with st.expander(f"Ferramenta {i + 1}"):
            codigo = st.text_input(f"Código da Ferramenta {i + 1}", key=f"cod{i}")
            descricao = ""
            if codigo:
                df_fer = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                if not df_fer.empty:
                    descricao = df_fer['Descricao'].values[0]
            st.text_input(f"Descrição {i + 1}", value=descricao, disabled=True, key=f"desc{i}")

            ferramentas_selecionadas.append((codigo, descricao))

    observacoes = st.text_area("Observações (opcional)")

    col1, col2 = st.columns([3,1])
    with col1:
        confirmar = st.form_submit_button("✅ Confirmar Movimentação")
    with col2:
        limpar = st.form_submit_button("🧹 Limpar")

# ——————————————————————————————————————————————————————————————
# Lógica de botões

if confirmar:
    if not nome:
        st.error("Informe uma matrícula válida antes de registrar.")
    else:
        ferramentas_validas = [(c, d) for c, d in ferramentas_selecionadas if c and d]
        if not ferramentas_validas:
            st.error("Informe pelo menos uma ferramenta válida antes de registrar.")
        else:
            agora = datetime.now(fuso)
            datahora = agora.strftime('%d/%m/%Y %H:%M:%S')
            ferramentas_str = "; ".join(f"{c} - {d}" for c, d in ferramentas_validas)

            # Registrar no CSV
            row = [datahora, matricula, nome, tipo, ferramentas_str, observacoes]
            with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(row)

            st.success("Movimentação registrada com sucesso!")

            # Gerar resumo
            resumo = f"""
===========================================================
                RESUMO DE MOVIMENTAÇÃO
===========================================================
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

===========================================================
"""

            st.session_state['resumo'] = resumo
            st.session_state['registrado'] = True

# Botão Limpar
if limpar:
    st.session_state['registrado'] = False
    st.experimental_rerun()

# Botão de Download só aparece após confirmar
if st.session_state.get('registrado'):
    st.download_button(
        label="📄 Baixar Resumo para Impressão",
        data=st.session_state['resumo'],
        file_name=f"resumo_{matricula}_{datetime.now(fuso).strftime('%Y%m%d%H%M%S')}.txt",
        mime="text/plain"
    )
