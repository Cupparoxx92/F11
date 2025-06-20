import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# ======================== CONFIGURAÇÕES ========================

st.set_page_config(
    page_title="Controle de Ferramentas",
    layout="wide",
)

# Fuso horário Brasil
fuso = pytz.timezone('America/Sao_Paulo')

# Inicializar variáveis de sessão
if 'mostrar_download' not in st.session_state:
    st.session_state.mostrar_download = False

if 'limpar' not in st.session_state:
    st.session_state.limpar = False


# =================== CARREGAR BASES ======================

# Colaboradores
try:
    colaboradores = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()
except:
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

# Ferramentas
try:
    ferramentas = pd.read_csv('ferramentas.csv', encoding='utf-8-sig')
    ferramentas.columns = ferramentas.columns.str.strip()
    ferramentas.rename(columns={'Descrição': 'Descricao'}, inplace=True)
except:
    ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao'])

# Movimentações
mov_file = 'movimentacao.csv'
mov_header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
if not os.path.exists(mov_file):
    pd.DataFrame(columns=mov_header).to_csv(mov_file, index=False, encoding='utf-8-sig')

# ===================== INTERFACE ======================

st.title("📦 Controle de Movimentação de Ferramentas")

# LIMPAR FORMULÁRIO
if st.button("🧹 Limpar Formulário"):
    st.session_state.limpar = True
    st.session_state.mostrar_download = False
    st.experimental_rerun()


with st.form("formulario"):
    # Matricula
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

    confirmar = st.form_submit_button("✅ Confirmar Movimentação")


    # ===================== AÇÃO AO CONFIRMAR ======================
    if confirmar:
        if not nome:
            st.error("⚠️ Informe uma matrícula válida antes de registrar.")
            st.session_state.mostrar_download = False
        else:
            ferramentas_validas = [(c, d) for c, d in selecionadas if c and d]
            if not ferramentas_validas:
                st.error("⚠️ Informe pelo menos uma ferramenta válida antes de registrar.")
                st.session_state.mostrar_download = False
            else:
                agora = datetime.now(fuso)
                datahora = agora.strftime('%d/%m/%Y %H:%M:%S')
                ferramentas_str = "; ".join([f"{c} - {d}" for c, d in ferramentas_validas])

                nova_linha = [datahora, matricula, nome, tipo, ferramentas_str, observacoes]

                with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(nova_linha)

                st.success("Movimentação registrada com sucesso!")

                # Gerar resumo para impressão
                resumo = f"""
========================================
           RESUMO DE MOVIMENTAÇÃO
========================================
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

Assinatura: ___________________________________________
========================================
"""

                # Salvar resumo em arquivo temporário
                with open("resumo_movimentacao.txt", "w", encoding="utf-8-sig") as file:
                    file.write(resumo)

                # Ativa o botão de download
                st.session_state.mostrar_download = True


# ==================== BOTÃO DE IMPRESSÃO ====================
if st.session_state.mostrar_download:
    with open("resumo_movimentacao.txt", "r", encoding="utf-8-sig") as file:
        conteudo = file.read()

    st.download_button(
        label="📄 Baixar Resumo para Impressão",
        data=conteudo,
        file_name=f"resumo_{matricula}_{datetime.now(fuso).strftime('%Y%m%d%H%M%S')}.txt",
        mime="text/plain"
    )

