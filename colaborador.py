import streamlit as st
import pandas as pd

def pagina_colaborador():
    st.subheader("👥 Gerenciamento de Colaboradores")

    # Função para carregar os colaboradores
    try:
        df = pd.read_csv('colaboradores.csv', encoding='utf-8-sig')
    except:
        df = pd.DataFrame(columns=['Matricula', 'Nome'])

    st.write("### 📜 Lista de Colaboradores")
    st.dataframe(df)

    st.write("---")
    st.write("### ➕ Adicionar Novo Colaborador")
    matricula = st.text_input("Matrícula")
    nome = st.text_input("Nome")

    if st.button("Adicionar Colaborador"):
        if matricula and nome:
            novo = pd.DataFrame([[matricula, nome]], columns=['Matricula', 'Nome'])
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv('colaboradores.csv', index=False, encoding='utf-8-sig')
            st.success(f"Colaborador {nome} adicionado com sucesso!")
            st.experimental_rerun()
        else:
            st.warning("Preencha todos os campos.")
