import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# ===============================================
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
mov_file = 'movimentacao.csv'
mov_header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']
if not os.path.exists(mov_file):
    pd.DataFrame(columns=mov_header).to_csv(mov_file, index=False, encoding='utf-8-sig')

# ===============================================
# Configuração da página
st.set_page_config(page_title="Controle de Ferramentas", layout="wide")
st.title("🔧 Controle de Ferramentas")

# ===============================================
# Variáveis de controle
if 'mostrar_download' not in st.session_state:
    st.session_state.mostrar_download = False

# ===============================================
# Formulário principal
with st.form("formulario"):
    st.subheader("Movimentação de Ferramentas")

    matricula = st.text_input("Matrícula")
    nome = ""
    if matricula:
        df_colab = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
        if not df_colab.empty:
            nome = df_colab['Nome'].values[0]
    st.text_input("Nome", value=nome, disabled=True)

    tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
    quantidade = st.number_input("Quantidade de Ferramentas", min_value=1, step=1, value=1)

    ferramentas_lista = []
    for i in range(quantidade):
        with st.expander(f"Ferramenta {i+1}"):
            cod = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")
            descricao = ""
            if cod:
                df_ferramenta = ferramentas[ferramentas['Codigo'].astype(str) == cod]
                if not df_ferramenta.empty:
                    descricao = df_ferramenta['Descricao'].values[0]
            st.text_input(f"Descrição {i+1}", value=descricao, disabled=True, key=f"desc{i}")
            ferramentas_lista.append((cod, descricao))

    obs = st.text_area("Observações (opcional)")

    col1, col2 = st.columns(2)
    enviar = col1.form_submit_button("✅ Confirmar Movimentação")
    limpar = col2.form_submit_button("🗑️ Limpar")

# ===============================================
# Ações do botão LIMPAR
if limpar:
    st.session_state.clear()
    st.experimental_rerun()

# ===============================================
# Ações do botão CONFIRMAR
if enviar:
    if not nome:
        st.error("⚠️ Matrícula inválida. Informe uma matrícula válida.")
    else:
        ferramentas_validas = [(c, d) for c, d in ferramentas_lista if c and d]
        if not ferramentas_validas:
            st.error("⚠️ Informe pelo menos uma ferramenta válida.")
        else:
            agora = datetime.now(fuso).strftime('%d/%m/%Y %H:%M:%S')
            ferramentas_str = "; ".join([f"{c} - {d}" for c, d in ferramentas_validas])

            nova_linha = [agora, matricula, nome, tipo, ferramentas_str, obs]
            with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(nova_linha)

            st.success("Movimentação registrada com sucesso!")

            # Gerar resumo para impressão
            resumo = f"""
============================================
            RESUMO DE MOVIMENTAÇÃO
============================================
Data/Hora: {agora}
Nome: {nome}
Matrícula: {matricula}
Tipo: {tipo}

Ferramentas:
"""
            for c, d in ferramentas_validas:
                resumo += f" - {c} - {d}\n"

            resumo += f"""
Observações: {obs}

Assinatura: ____________________________________________

============================================
"""

            with open("resumo_movimentacao.txt", "w", encoding="utf-8-sig") as file:
                file.write(resumo)

            st.session_state.mostrar_download = True

# ===============================================
# Download do resumo
if st.session_state.mostrar_download:
    with open("resumo_movimentacao.txt", "r", encoding="utf-8-sig") as file:
        conteudo = file.read()
    st.download_button(
        label="📄 Baixar Resumo para Impressão",
        data=conteudo,
        file_name=f"resumo_{matricula}_{datetime.now(fuso).strftime('%Y%m%d%H%M%S')}.txt",
        mime="text/plain"
    )
