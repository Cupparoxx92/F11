import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os
import subprocess

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Login - Ferramentaria",
    layout="centered",
    page_icon="🔐"
)

st.title("🔐 Acesso ao Sistema de Ferramentaria")

# =========================
# Arquivos
# =========================
arquivo_colaboradores = 'colaboradores.csv'
arquivo_log = 'loger.csv'

# Inicializar log se não existir
if not os.path.exists(arquivo_log):
    pd.DataFrame(columns=['DataHora', 'Matricula', 'Nome', 'Ação', 'Detalhes']).to_csv(arquivo_log, index=False, encoding='utf-8-sig')

# Carregar colaboradores
try:
    colaboradores = pd.read_csv(arquivo_colaboradores, encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()
except:
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

# =========================
# Formulário de Login
# =========================
st.subheader("Digite sua matrícula para acessar:")

matricula = st.text_input("Matrícula")

if st.button("🔓 Acessar Sistema"):
    if not matricula:
        st.error("⚠️ Matrícula é obrigatória.")
    else:
        user = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
        if not user.empty:
            nome = user['Nome'].values[0]

            # Registrar no log
            fuso = pytz.timezone('America/Sao_Paulo')
            datahora = datetime.now(fuso).strftime('%d/%m/%Y %H:%M:%S')

            df_log = pd.DataFrame([{
                'DataHora': datahora,
                'Matricula': matricula,
                'Nome': nome,
                'Ação': 'Login',
                'Detalhes': 'Acesso ao sistema'
            }])
            df_log.to_csv(arquivo_log, mode='a', index=False, header=False, encoding='utf-8-sig')

            st.success(f"✅ Bem-vindo, {nome}!")
            st.info("🚀 Clique abaixo para acessar o sistema.")

            if st.button("➡️ Ir para o Sistema"):
                subprocess.Popen(["streamlit", "run", "principal.py"])
                st.stop()  # Para essa página e abre o principal
        else:
            st.error("❌ Matrícula não encontrada. Verifique com o administrador.")

