import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

from relatorio import pagina_relatorio
from colaborador import pagina_colaborador
from ferramenta import pagina_ferramenta

# =========================
# CONFIGURAÇÕES INICIAIS
# =========================
st.set_page_config(
    page_title="Controle de Ferramentaria",
    layout="wide",
    page_icon="🛠️"
)

st.title("🛠️ Controle de Ferramentaria")

# =========================
# VARIÁVEIS E ARQUIVOS
# =========================
fuso = pytz.timezone('America/Sao_Paulo')

arquivo_movimentacao = 'movimentacao.csv'
arquivo_colaboradores = 'colaboradores.csv'
arquivo_ferramentas = 'ferramentas.csv'

cabecalho_movimentacao = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'CodigoFerramenta', 'DescricaoFerramenta', 'Observacoes']


# =========================
# FUNÇÕES AUXILIARES
# =========================
def inicializar_movimentacao():
    if not os.path.exists(arquivo_movimentacao):
        pd.DataFrame(columns=cabecalho_movimentacao).to_csv(arquivo_movimentacao, index=False, encoding='utf-8-sig')


def carregar_colaboradores():
    try:
        return pd.read_csv(arquivo_colaboradores, encoding='utf-8-sig')
    except:
        return pd.DataFrame(columns=['Matricula', 'Nome'])


def carregar_ferramentas():
    try:
        return pd.read_csv(arquivo_ferramentas, encoding='utf-8-sig')
    except:
        return pd.DataFrame(columns=['Codigo', 'Descricao', 'StatusConserto'])


def ferramenta_disponivel(codigo):
    df_mov = pd.read_csv(arquivo_movimentacao, encoding='utf-8-sig') if os.path.exists(arquivo_movimentacao) else pd.DataFrame(columns=cabecalho_movimentacao)
    df_ferr = carregar_ferramentas()

    # Verifica se está em conserto
    ferramenta = df_ferr[df_ferr['Codigo'].astype(str) == str(codigo)]
    if not ferramenta.empty and ferramenta['StatusConserto'].values[0] == 'Em Conserto':
        return False

    # Verifica última movimentação
    df = df_mov[df_mov['CodigoFerramenta'].astype(str) == str(codigo)]
    if df.empty:
        return True
    ultima = df.iloc[-1]
    return ultima['Tipo'] == 'Devolução'


def registrar_movimentacao(matricula, nome, tipo, codigo, descricao, observacoes):
    inicializar_movimentacao()
    datahora = datetime.now(fuso).strftime('%d/%m/%Y %H:%M:%S')

    dados = {
        'DataHora': datahora,
        'Matricula': matricula,
        'Nome': nome,
        'Tipo': tipo,
        'CodigoFerramenta': codigo,
        'DescricaoFerramenta': descricao,
        'Observacoes': observacoes
    }

    df = pd.DataFrame([dados])
    df.to_csv(arquivo_movimentacao, mode='a', header=not os.path.exists(arquivo_movimentacao), index=False, encoding='utf-8-sig')

    return datahora


# =========================
# MENU LATERAL
# =========================
menu = st.sidebar.radio("Menu", ["Movimentação", "Colaborador", "Ferramenta", "Relatório"])

# =========================
# CARREGAMENTO DE DADOS
# =========================
colaboradores = carregar_colaboradores()
ferramentas = carregar_ferramentas()


# =========================
# MOVIMENTAÇÃO
# =========================
if menu == "Movimentação":
    st.subheader("📦 Movimentação de Ferramentas")

    with st.form("form_movimentacao"):
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
            quantidade = st.number_input("Quantidade de Ferramentas", min_value=1, step=1, value=1)

        ferramentas_selecionadas = []
        erro = False

        for i in range(quantidade):
            with st.expander(f"Ferramenta {i + 1}"):
                codigo = st.text_input(f"Código da Ferramenta {i + 1}", key=f"cod_{i}")
                descricao = ""

                if codigo:
                    df_ferr = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                    if not df_ferr.empty:
                        descricao = df_ferr['Descricao'].values[0]

                        if tipo == "Retirada" and not ferramenta_disponivel(codigo):
                            st.error(f"❌ A ferramenta {codigo} - {descricao} não está disponível (retirada ou em conserto).")
                            erro = True
                            descricao = ""

                    st.text_input(f"Descrição {i + 1}", value=descricao, disabled=True, key=f"desc_{i}")
                    ferramentas_selecionadas.append((codigo, descricao))

        observacoes = st.text_area("Observações (opcional)")
        sem_obs = st.checkbox("✔️ Sem Observações")

        enviar = st.form_submit_button("✅ Confirmar Movimentação")
        limpar = st.form_submit_button("🧹 Limpar")

    if limpar:
        st.experimental_rerun()

    if enviar:
        if not nome:
            st.error("⚠️ Matrícula inválida.")
        elif erro:
            st.error("⚠️ Corrija os erros nas ferramentas.")
        elif not observacoes and not sem_obs:
            st.error("⚠️ Preencha observações ou marque 'Sem Observações'.")
        else:
            for codigo, descricao in ferramentas_selecionadas:
                if codigo and descricao:
                    registrar_movimentacao(
                        matricula=matricula,
                        nome=nome,
                        tipo=tipo,
                        codigo=codigo,
                        descricao=descricao,
                        observacoes=observacoes if observacoes else "Sem Observações"
                    )
            st.success("✅ Movimentação registrada com sucesso.")


# =========================
# COLABORADOR
# =========================
elif menu == "Colaborador":
    pagina_colaborador()


# =========================
# FERRAMENTA
# =========================
elif menu == "Ferramenta":
    pagina_ferramenta()


# =========================
# RELATÓRIO
# =========================
elif menu == "Relatório":
    pagina_relatorio()
