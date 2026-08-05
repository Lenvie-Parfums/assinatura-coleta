import streamlit as st

st.title("Teste de importação")

try:
    from utils.assinatura import AssinaturaCanvas
    st.success("✅ assinatura OK")
except Exception as e:
    st.error(f"❌ assinatura: {e}")

try:
    from utils.formulario import FormularioRetirada
    st.success("✅ formulario OK")
except Exception as e:
    st.error(f"❌ formulario: {e}")

try:
    from utils.gerador_pdf import GeradorPDF
    st.success("✅ gerador_pdf OK")
except Exception as e:
    st.error(f"❌ gerador_pdf: {e}")

try:
    from utils.drive import upload_pdf_google_drive
    st.success("✅ drive OK")
except Exception as e:
    st.error(f"❌ drive: {e}")

try:
    from utils.alterar_status import ConsultarNF
    st.success("✅ alterar_status OK")
except Exception as e:
    st.error(f"❌ alterar_status: {e}")