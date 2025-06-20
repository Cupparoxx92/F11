import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# ==============================
# CONFIGURAÇÕES INICIAIS
# ==============================
st.set_page_config(page_title="Controle de Ferramentas", layout="wide")

# Fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# Inicializar controle do download
if 'mostrar_download' not in st.session_state:
    st.session_state.mostrar_download = False

# ==============================
# CARREGAMENTO DOS DADOS
# ==============================

# Arquivos principais
arquivo_colaboradores = 'colaboradores.csv'
arquivo_ferramentas = 'ferramentas.csv'
arquivo_movimentacoes = 'movimentacao.csv'

# Carregar colaboradores
try:
    colaboradores = pd.read_csv(arquivo_colaboradores, encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()
except:
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

# Carregar ferramentas
try:
    ferramentas = pd.read_csv(arquivo_ferramentas, encoding='utf-8-sig')
    ferramentas.columns = ferramentas.columns.str.strip()
    ferramentas.rename(columns={'Descrição': 'Descricao'}, inplace=True)
except:
    ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao'])

# Criar arquivo movimentação se não existir
if not os.path.exists(arquivo_movimentacoes):
    pd.DataFrame(columns=['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']) \
      .to_csv(arquivo_movimentacoes, index=False, encoding='utf-8-sig')

# ==============================
# INTERFACE
# ==============================

st.title("🔧 Controle de Movimentação de Ferramentas")

with st.form("form_mov"):

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

    col_btn1, col_btn2 = st.columns(2)
    confirmar = col_btn1.form_submit_button("✅ Confirmar Movimentação")
    limpar = col_btn2.form_submit_button("🧹 Limpar")

    # ==============================
    # AÇÕES DOS BOTÕES
    # ==============================

    if confirmar:
        if not nome:
            st.error("Informe uma matrícula válida antes de registrar.")
        else:
            validas = [(c, d) for c, d in selecionadas if c and d]
            if not validas:
                st.error("Informe pelo menos uma ferramenta válida antes de registrar.")
            else:
                agora = datetime.now(fuso)
                datahora = agora.strftime('%d/%m/%Y %H:%M:%S')

                ferramentas_str = "; ".join([f"{c} - {d}" for c, d in validas])

                nova_linha = [datahora, matricula, nome, tipo, ferramentas_str, observacoes]

                # Salvar no CSV
                with open(arquivo_movimentacoes, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(nova_linha)

                st.success("Movimentação registrada com sucesso!")

                # Gerar resumo para impressão
                resumo = f"""
====================================================
                RESUMO DE MOVIMENTAÇÃO
====================================================
Data/Hora: {datahora}
Nome: {nome}
Matrícula: {matricula}
Tipo: {tipo}

Ferramentas:
"""
                for c, d in validas:
                    resumo += f" - {c} - {d}\n"

                resumo += f"""
\nObservações: {observacoes}

\nAssinatura: ____________________________________________

====================================================
"""

                with open("resumo_movimentacao.txt", "w", encoding="utf-8-sig") as file:
                    file.write(resumo)

                st.session_state.mostrar_download = True

    if limpar:
        st.session_state.mostrar_download = False
        st.experimental_rerun()

# ==============================
# BOTÃO DE DOWNLOAD DO RESUMO
# ==============================

if st.session_state.mostrar_download:
    with open("resumo_movimentacao.txt", "r", encoding="utf-8-sig") as file:
        conteudo = file.read()
    st.download_button(
        label="📄 Baixar Resumo para Impressão",
        data=conteudo,
        file_name=f"resumo_{matricula}_{datetime.now(fuso).strftime('%Y%m%d%H%M%S')}.txt",
        mime="text/plain"
    )
