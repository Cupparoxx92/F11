import streamlit as st
from datetime import datetime
import pandas as pd
import pytz

# ——————————————————————————————————————————————————————————————
# 1) Defina o fuso horário (ex.: São Paulo)
fuso = pytz.timezone('America/Sao_Paulo')

# 2) Carregue e normalize a base de colaboradores
try:
    colaboradores = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
    colaboradores.columns = colaboradores.columns.str.strip()
except Exception as e:
    st.error(f"Não foi possível ler 'colaboradores.csv': {e}")
    colaboradores = pd.DataFrame(columns=['Matricula', 'Nome'])

# 3) Carregue e normalize a base de ferramentas
try:
    ferramentas = pd.read_csv('ferramentas.csv', encoding='utf-8-sig')
    ferramentas.columns = ferramentas.columns.str.strip()
    ferramentas.rename(columns={'Descrição': 'Descricao'}, inplace=True)
except Exception as e:
    st.error(f"Não foi possível ler 'ferramentas.csv': {e}")
    ferramentas = pd.DataFrame(columns=['Codigo', 'Descricao'])

# ——————————————————————————————————————————————————————————————
# Configuração geral da página
st.set_page_config(
    page_title="Ferramentaria",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Ferramentaria")

# Menu lateral
menu = st.sidebar.radio("Menu", ["Movimentação", "Colaborador", "Ferramenta", "Relatório"])

# ——————————————————————————————————————————————————————————————
if menu == "Movimentação":
    st.header("Movimentação")

    # Matrícula → Nome automático
    c1, c2 = st.columns(2)
    with c1:
        matricula = st.text_input("Matrícula")
    with c2:
        nome = ""
        if matricula:
            df = colaboradores[ colaboradores['Matricula'].astype(str) == matricula ]
            nome = df['Nome'].values[0] if not df.empty else "Matrícula não encontrada"
        st.text_input("Nome", value=nome, disabled=True)

    # Tipo de movimentação
    tipo = st.selectbox("Tipo de Movimentação", ["Retirada", "Devolução"])

    st.markdown("---")
    st.subheader("Ferramentas")

    selecionadas = []
    qtd = st.number_input("Quantidade de Ferramentas", min_value=1, value=1, step=1)

    for i in range(qtd):
        with st.expander(f"Ferramenta {i+1}"):
            f1, f2 = st.columns(2)
            with f1:
                codigo = st.text_input(f"Código {i+1}", key=f"cod_{i}")
            with f2:
                desc = ""
                if codigo:
                    df2 = ferramentas[ ferramentas['Codigo'].astype(str) == codigo ]
                    desc = df2['Descricao'].values[0] if not df2.empty else "Código não encontrado"
                st.text_input(f"Descrição {i+1}", value=desc, disabled=True)
            selecionadas.append((codigo, desc))

    st.markdown("---")
    observacoes = st.text_area("Observações (opcional)")

    if st.button("Confirmar Movimentação"):
        agora = datetime.now(fuso)
        data_hora = agora.strftime('%d/%m/%Y %H:%M:%S')

        st.success("Movimentação registrada com sucesso!")
        st.subheader("Resumo:")
        st.write(f"- **Data/Hora:** {data_hora}")
        st.write(f"- **Matrícula:** {matricula} — **Nome:** {nome}")
        st.write(f"- **Tipo:** {tipo}")
        st.write(f"- **Observações:** {observacoes or '—'}")
        st.write("**Ferramentas:**")
        for idx, (c, d) in enumerate(selecionadas, start=1):
            st.write(f"{idx}. {c} ― {d}")

# ——————————————————————————————————————————————————————————————
elif menu == "Colaborador":
    st.header("Colaborador")
    st.info("Página em construção.")

elif menu == "Ferramenta":
    st.header("Ferramenta")
    st.info("Página em construção.")

elif menu == "Relatório":
    st.header("Relatório")
    st.info("Página em construção.")
