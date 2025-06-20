import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# ==========================================
# Configurações iniciais
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
arquivo_mov = 'movimentacao.csv'
cabecalho = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
if not os.path.exists(arquivo_mov):
    pd.DataFrame(columns=cabecalho).to_csv(arquivo_mov, index=False, encoding='utf-8-sig')

# ==========================================
# Página
st.set_page_config(page_title="Controle de Ferramentas", layout="wide")
st.title("🔧 Controle de Movimentação de Ferramentas")

# Estado para controlar exibição do resumo
if 'mostrar_resumo' not in st.session_state:
    st.session_state.mostrar_resumo = False

# ==========================================
# Formulário principal
with st.form("movimentacao"):

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        matricula = st.text_input("Matrícula")
    with col2:
        tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
    with col3:
        qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)

    nome = ""
    if matricula:
        busca = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
        if not busca.empty:
            nome = busca['Nome'].values[0]
    st.text_input("Nome", value=nome, disabled=True)

    selecionadas = []
    for i in range(qtd):
        with st.expander(f"Ferramenta {i+1}"):
            cod = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")
            desc = ""
            if cod:
                busca = ferramentas[ferramentas['Codigo'].astype(str) == cod]
                if not busca.empty:
                    desc = busca['Descricao'].values[0]
            st.text_input(f"Descrição {i+1}", value=desc, disabled=True, key=f"desc{i}")
            selecionadas.append((cod, desc))

    observacoes = st.text_area("Observações (opcional)")

    col4, col5 = st.columns([1, 1])
    confirmar = col4.form_submit_button("✅ Confirmar Movimentação")
    limpar = col5.form_submit_button("🧹 Limpar")

    # ==========================================
    # Ação do botão Limpar
    if limpar:
        st.session_state.mostrar_resumo = False
        st.experimental_rerun()

    # ==========================================
    # Ação do botão Confirmar
    if confirmar:
        if not nome:
            st.error("Informe uma matrícula válida antes de registrar.")
            st.session_state.mostrar_resumo = False
        else:
            validas = [(c, d) for c, d in selecionadas if c and d]
            if not validas:
                st.error("Informe pelo menos uma ferramenta válida antes de registrar.")
                st.session_state.mostrar_resumo = False
            else:
                agora = datetime.now(fuso)
                datahora = agora.strftime('%d/%m/%Y %H:%M:%S')
                ferramentas_txt = "; ".join([f"{c} - {d}" for c, d in validas])

                nova_linha = [datahora, matricula, nome, tipo, ferramentas_txt, observacoes]
                with open(arquivo_mov, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(nova_linha)

                st.success("Movimentação registrada com sucesso!")

                # Criar resumo para impressão
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
                for c, d in validas:
                    resumo += f" - {c} - {d}\n"

                resumo += f"""
                \nObservações: {observacoes}
                \n\nAssinatura: ____________________________________________
                ============================================
                """

                with open("resumo_movimentacao.txt", "w", encoding="utf-8-sig") as file:
                    file.write(resumo)

                st.session_state.mostrar_resumo = True

# ==========================================
# Mostrar botão de download APÓS confirmação
if st.session_state.mostrar_resumo:
    with open("resumo_movimentacao.txt", "r", encoding="utf-8-sig") as file:
        conteudo = file.read()
    st.download_button(
        label="📄 Baixar Resumo para Impressão",
        data=conteudo,
        file_name=f"resumo_{matricula}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt",
        mime="text/plain"
    )
