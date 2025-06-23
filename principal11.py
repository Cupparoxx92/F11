import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

from relatorio import pagina_relatorio
from colaborador import pagina_colaborador
from ferramenta import pagina_ferramenta

# =========================
# CONFIGURAÇÕES
# =========================
st.set_page_config(
    page_title="Ferramentaria - Controle de Movimentação",
    layout="wide",
    page_icon="🛠️",
    initial_sidebar_state="expanded"
)

st.title("🛠️ Controle de Ferramentaria")

# Fuso horário
fuso = pytz.timezone('America/Sao_Paulo')

# Arquivos
arquivo_movimentacao = 'movimentacao.csv'
arquivo_colaboradores = 'colaboradores.csv'
arquivo_ferramentas = 'ferramentas.csv'

# Cabeçalhos
cabecalho_mov = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'CodigoFerramenta', 'DescricaoFerramenta', 'Observacoes']


# =========================
# FUNÇÕES AUXILIARES
# =========================
def inicializar_arquivo_movimentacao():
    if not os.path.exists(arquivo_movimentacao):
        pd.DataFrame(columns=cabecalho_mov).to_csv(arquivo_movimentacao, index=False, encoding='utf-8-sig')


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
    ferramentas = carregar_ferramentas()
    status = ferramentas.loc[ferramentas['Codigo'].astype(str) == str(codigo), 'StatusConserto']

    if not status.empty and status.values[0] == 'Em Conserto':
        return False

    if not os.path.exists(arquivo_movimentacao):
        return True

    mov = pd.read_csv(arquivo_movimentacao, encoding='utf-8-sig')
    mov = mov[mov['CodigoFerramenta'].astype(str) == str(codigo)]

    if mov.empty:
        return True

    ultima = mov.iloc[-1]
    return ultima['Tipo'] != 'Retirada'


def registrar_movimentacao(matricula, nome, tipo, codigo, descricao, observacoes):
    inicializar_arquivo_movimentacao()
    datahora = datetime.now(fuso).strftime('%Y-%m-%d %H:%M:%S')

    registro = {
        'DataHora': datahora,
        'Matricula': matricula,
        'Nome': nome,
        'Tipo': tipo,
        'CodigoFerramenta': codigo,
        'DescricaoFerramenta': descricao,
        'Observacoes': observacoes
    }

    df = pd.DataFrame([registro])
    df.to_csv(arquivo_movimentacao, mode='a', header=not os.path.exists(arquivo_movimentacao),
              index=False, encoding='utf-8-sig')

    return datahora


# =========================
# MENU LATERAL
# =========================
menu = st.sidebar.radio(
    "📑 Menu",
    ["Movimentação", "Colaborador", "Ferramenta", "Relatório"]
)

# =========================
# CARREGAMENTO DE DADOS
# =========================
colaboradores = carregar_colaboradores()
ferramentas = carregar_ferramentas()


# =========================
# PÁGINAS DO MENU
# =========================

# >>>>>>>>> MOVIMENTAÇÃO <<<<<<<<<<<
if menu == "Movimentação":
    st.subheader("📦 Movimentação de Ferramentas")

    with st.form("formulario", clear_on_submit=False):
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
        erro_ferramenta = False

        for i in range(qtd):
            with st.expander(f"🔧 Ferramenta {i + 1}"):
                codigo = st.text_input(f"Código da Ferramenta {i + 1}", key=f"cod_{i}")
                desc = ""
                if codigo:
                    df_ferr = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                    if not df_ferr.empty:
                        desc = df_ferr['Descricao'].values[0]

                        if tipo == "Retirada":
                            if not ferramenta_disponivel(codigo):
                                st.error(
                                    f"⚠️ A ferramenta {codigo} - {desc} está retirada ou em conserto!")
                                erro_ferramenta = True
                                desc = ""

                st.text_input(f"Descrição {i + 1}", value=desc, disabled=True, key=f"desc_{i}")
                selecionadas.append((codigo, desc))

        observacoes = st.text_area("Observações (opcional)")
        sem_obs = st.checkbox("✔️ Sem Observações")

        submit = st.form_submit_button("✅ Confirmar Movimentação")
        limpar = st.form_submit_button("🧹 Limpar")

    if limpar:
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

    if submit:
        if not nome:
            st.error("⚠️ Informe uma matrícula válida antes de registrar.")
        elif erro_ferramenta:
            st.error("⚠️ Corrija os erros nas ferramentas antes de registrar.")
        elif not observacoes and not sem_obs:
            st.error("⚠️ Preencha Observações ou marque 'Sem Observações'.")
        else:
            ferramentas_validas = [(c, d) for c, d in selecionadas if c and d]
            if not ferramentas_validas:
                st.error("⚠️ Informe pelo menos uma ferramenta válida antes de registrar.")
            else:
                for cod, desc in ferramentas_validas:
                    registrar_movimentacao(
                        matricula=matricula,
                        nome=nome,
                        tipo=tipo,
                        codigo=cod,
                        descricao=desc,
                        observacoes=observacoes if observacoes else "Sem Observações"
                    )

                st.success("✅ Movimentação registrada com sucesso!")

# >>>>>>>>> COLABORADOR <<<<<<<<<<<
elif menu == "Colaborador":
    pagina_colaborador()

# >>>>>>>>> FERRAMENTA <<<<<<<<<<<
elif menu == "Ferramenta":
    pagina_ferramenta()

# >>>>>>>>> RELATÓRIO <<<<<<<<<<<
elif menu == "Relatório":
    pagina_relatorio()
