import streamlit as st
from utils.assinatura import AssinaturaCanvas
from utils.formulario import FormularioRetirada
from utils.gerador_pdf import GeradorPDF
from utils.alterar_status import ConsultarNF
import re
import time

st.set_page_config(page_title="Coleta Transportadora", layout="centered")
st.title("📦 Romaneio de carga")

if "dados_formulario" not in st.session_state:

    form = FormularioRetirada()
    dados = form.exibir_formulario()

    if dados:
        st.session_state["dados_formulario"] = dados
        st.rerun()

else:
    dados = st.session_state["dados_formulario"]
    st.success("✅ Dados do formulário recebidos. Agora colete a assinatura.")

    assinatura = AssinaturaCanvas().capturar_assinatura()

    if assinatura is not None:
        notas = dados["pedido"]
        lista_notas = [p.strip() for p in re.split(r"[,\-]", notas) if p.strip()]

        if st.button("📄 Gerar PDF e Atualizar Omie"):
            pdf = GeradorPDF(dados, assinatura)
            pdf_stream = pdf.gerar_pdf()

            st.download_button(
                label="⬇ Baixar Comprovante",
                data=pdf_stream,
                file_name=f"comprovante_{dados['pedido']}.pdf",
                mime="application/pdf"
            )

            for nota in lista_notas:
                try:
                    st.info(f"Atualizando Nota no Omie: {nota}")
                    resultado = ConsultarNF(nota)
                    time.sleep(1)

                    if resultado == True:
                        st.success(f"✅ Nota {nota} processada com sucesso!")
                    else:
                        st.error(f"❌ Erro para atualizar a nota: {nota} - {resultado}")
                except Exception as e:
                    st.error(f"❌ Erro para atualizar a nota: {nota} - {e}")

            st.success("✅ Todas as notas foram processadas!")

    else:
        st.warning("✍️ Por favor, assine no campo acima.")

    if st.button("🔄 Nova Retirada"):
        st.session_state.clear()
        st.rerun()