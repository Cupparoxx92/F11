# Variável para armazenar o resumo após registro
resumo_movimentacao = ""

# Dentro do st.form:
with st.form("form_mov"):
    # ... (todos os campos do formulário)

    submit = st.form_submit_button("Confirmar Movimentação")

    if submit:
        if not nome:
            st.error("Informe uma matrícula válida antes de registrar.")
        else:
            valid = [(c, d) for c, d in selecionadas if c and d]
            if not valid:
                st.error("Informe pelo menos uma ferramenta válida antes de registrar.")
            else:
                agora = datetime.now(fuso)
                datahora = agora.strftime('%d/%m/%Y %H:%M:%S')
                tools_str = "; ".join(f"{c} - {d}" for c, d in valid)

                row = [datahora, matricula, nome, tipo, tools_str, observacoes]
                with open(mov_file, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)

                st.success("Movimentação registrada com sucesso!")

                # Gera o resumo e salva na variável
                resumo_movimentacao = f"""
============================================
           RESUMO DE MOVIMENTAÇÃO
============================================
Data/Hora: {datahora}
Nome: {nome}
Matrícula: {matricula}
Tipo: {tipo}

Ferramentas:
"""
                for c, d in valid:
                    resumo_movimentacao += f" - {c} - {d}\n"

                resumo_movimentacao += f"""
Observações: {observacoes}

Assinatura: ____________________________________________

============================================
"""

# Fora do st.form
if resumo_movimentacao:
    st.text_area("Resumo da Movimentação", resumo_movimentacao, height=300)
    st.download_button(
        label="📄 Baixar Resumo para Impressão",
        data=resumo_movimentacao,
        file_name=f"resumo_{matricula}_{datetime.now(fuso).strftime('%Y%m%d%H%M%S')}.txt",
        mime="text/plain"
    )

