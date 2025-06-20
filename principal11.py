import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import os
import csv

# Fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# Arquivo de movimentações
mov_file = 'movimentacao.csv'
mov_header = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']

# Garante que o arquivo exista
if not os.path.exists(mov_file):
    pd.DataFrame(columns=mov_header).to_csv(mov_file, index=False, encoding='utf-8-sig')

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

# Streamlit
st.set_page_config(page_title="Ferramentaria", layout="wide")
st.title("Movimentação de Ferramentas")

with st.form("formulario"):

    matricula = st.text_input("Matrícula")
    nome = ""

    if matricula:
        busca = colaboradores[colaboradores['Matricula'].astype(str) == matricula]
        if not busca.empty:
            nome = busca['Nome'].values[0]
    st.text_input("Nome", value=nome, disabled=True)

    tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])
    qtd = st.number_input("Quantidade de Ferramentas", min_value=1, step=1, value=1)

    ferramentas_selecionadas = []

    for i in range(qtd):
        with st.expander(f"Ferramenta {i+1}"):
            codigo = st.text_input(f"Código da Ferramenta {i+1}", key=f"cod{i}")
            descricao = ""
            if codigo:
                busca_ferramenta = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                if not busca_ferramenta.empty:
                    descricao = busca_ferramenta['Descricao'].values[0]
            st.text_input(f"Descrição {i+1}", value=descricao, disabled=True, key=f"desc{i}")
            ferramentas_selecionadas.append((codigo, descricao))

    observacoes = st.text_area("Observações (opcional)")

    enviar = st.form_submit_button("Confirmar Movimentação")

    if enviar:
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

                registro = [datahora, matricula, nome, tipo, ferramentas_str, observacoes]

                # Gravar no CSV
                with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(registro)

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

Assinatura: ____________________________________________

========================================
"""

                with open("resumo_movimentacao.txt", "w", encoding="utf-8-sig") as file:
                    file.write(resumo)

                with open("resumo_movimentacao.txt", "r", encoding="utf-8-sig") as file:
                    conteudo = file.read()
                    st.download_button(
                        label="📄 Baixar Resumo para Impressão",
                        data=conteudo,
                        file_name=f"resumo_{matricula}_{agora.strftime('%Y%m%d%H%M%S')}.txt",
                        mime="text/plain"
                    )
