import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# =========================
# CONFIGURAÇÕES INICIAIS
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

# Cabeçalho da movimentação
cabecalho = ['DataHora', 'Matricula', 'Nome', 'Tipo', 'Ferramentas', 'Observacoes']

# =========================
# FUNÇÕES AUXILIARES
# =========================
def inicializar_arquivo_movimentacao():
    if not os.path.exists(arquivo_movimentacao):
        pd.DataFrame(columns=cabecalho).to_csv(arquivo_movimentacao, index=False, encoding='utf-8-sig')

def carregar_colaboradores():
    try:
        df = pd.read_csv(arquivo_colaboradores, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=['Matricula', 'Nome'])

def carregar_ferramentas():
    try:
        df = pd.read_csv(arquivo_ferramentas, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        df.rename(columns={'Descrição': 'Descricao'}, inplace=True)
        return df
    except:
        return pd.DataFrame(columns=['Codigo', 'Descricao'])

def registrar_movimentacao(matricula, nome, tipo, ferramentas, observacoes):
    inicializar_arquivo_movimentacao()
    datahora = datetime.now(fuso).strftime('%d/%m/%Y %H:%M:%S')

    dados = {
        'DataHora': datahora,
        'Matricula': matricula,
        'Nome': nome,
        'Tipo': tipo,
        'Ferramentas': ferramentas,
        'Observacoes': observacoes
    }

    df = pd.DataFrame([dados])
    df.to_csv(arquivo_movimentacao, mode='a', index=False, header=False, encoding='utf-8-sig')

    return datahora

def gerar_resumo(datahora, matricula, nome, tipo, ferramentas, observacoes):
    resumo = f"""
    =============================================
                 RESUMO DE MOVIMENTAÇÃO
    =============================================
    Data/Hora: {datahora}
    Nome: {nome}
    Matrícula: {matricula}
    Tipo de Movimentação: {tipo}

    Ferramentas:
    """
    for c, d in ferramentas:
        resumo += f" - {c} - {d}\n"

    resumo += f"""
    \nObservações: {observacoes}
    \n\nAssinatura: ____________________________________________
    =============================================
    """
    return resumo

def ferramenta_disponivel(codigo):
    """Verifica se a ferramenta está disponível para retirada"""
    if not os.path.exists(arquivo_movimentacao):
        return True  # Se não tem registro, está disponível

    df = pd.read_csv(arquivo_movimentacao, encoding='utf-8-sig')
    df = df[df['Ferramentas'].str.contains(str(codigo), na=False)]

    if df.empty:
        return True  # Nunca foi movimentada, está disponível

    ultima_mov = df.iloc[-1]  # Pega o último registro dessa ferramenta
    if 'Retirada' in ultima_mov['Tipo']:
        return False  # Está fora
    else:
        return True  # Está disponível


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
        erro_ferramenta = False  # Flag para impedir envio se tiver erro

        for i in range(qtd):
            with st.expander(f"Ferramenta {i + 1}"):
                codigo = st.text_input(f"Código da Ferramenta {i + 1}", key=f"cod_{i}")
                desc = ""
                if codigo:
                    df_ferr = ferramentas[ferramentas['Codigo'].astype(str) == codigo]
                    if not df_ferr.empty:
                        desc = df_ferr['Descricao'].values[0]

                        # Verificar disponibilidade da ferramenta
                        if tipo == "Retirada":
                            if not ferramenta_disponivel(codigo):
                                st.error(f"⚠️ A ferramenta {codigo} - {desc} já está retirada! Faça a devolução antes.")
                                erro_ferramenta = True
                                desc = ""

                st.text_input(f"Descrição {i + 1}", value=desc, disabled=True, key=f"desc_{i}")
                selecionadas.append((codigo, desc))

        observacoes = st.text_area("Observações (opcional)")

        col3, col4 = st.columns([1, 5])
        submit = col3.form_submit_button("✅ Confirmar Movimentação")
        limpar = col4.form_submit_button("🧹 Limpar")

    if limpar:
        st.rerun()

    if submit:
        if not nome:
            st.error("⚠️ Informe uma matrícula válida antes de registrar.")
        elif erro_ferramenta:
            st.error("⚠️ Corrija os erros nas ferramentas antes de registrar.")
        else:
            ferramentas_validas = [(c, d) for c, d in selecionadas if c and d]
            if not ferramentas_validas:
                st.error("⚠️ Informe pelo menos uma ferramenta válida antes de registrar.")
            else:
                ferramentas_str = "; ".join([f"{c} - {d}" for c, d in ferramentas_validas])
                datahora = registrar_movimentacao(
                    matricula=matricula,
                    nome=nome,
                    tipo=tipo,
                    ferramentas=ferramentas_str,
                    observacoes=observacoes
                )

                st.success("✅ Movimentação registrada com sucesso!")

                resumo = gerar_resumo(datahora, matricula, nome, tipo, ferramentas_validas, observacoes)

                st.download_button(
                    label="📄 Baixar Resumo para Impressão",
                    data=resumo,
                    file_name=f"resumo_{matricula}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt",
                    mime="text/plain"
                )

# >>>>>>>>> COLABORADOR <<<<<<<<<<<
elif menu == "Colaborador":
    st.subheader("👥 Gerenciamento de Colaboradores")
    st.info("🔧 Página em construção. Podemos criar aqui: adicionar, editar e excluir colaboradores.")

# >>>>>>>>> FERRAMENTA <<<<<<<<<<<
elif menu == "Ferramenta":
    st.subheader("🛠️ Gerenciamento de Ferramentas")
    st.info("🔧 Página em construção. Podemos criar aqui: cadastro, edição e controle de ferramentas.")

# >>>>>>>>> RELATÓRIO <<<<<<<<<<<
elif menu == "Relatório":
    st.subheader("📑 Relatório de Movimentações")

    try:
        df_mov = pd.read_csv(arquivo_movimentacao, encoding='utf-8-sig')
        st.dataframe(df_mov)

        st.download_button(
            label="⬇️ Baixar CSV de Movimentações",
            data=df_mov.to_csv(index=False, encoding='utf-8-sig'),
            file_name="relatorio_movimentacoes.csv",
            mime="text/csv"
        )
    except:
        st.warning("⚠️ Nenhuma movimentação registrada ainda.")
