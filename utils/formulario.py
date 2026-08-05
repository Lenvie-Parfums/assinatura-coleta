import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

class FormularioRetirada:
    def exibir_formulario(self):
        with st.form("form_retirada"):
            transportadora = st.text_input("Nome da transportadora")
            motorista = st.text_input("Nome do motorista")
            cpf = st.text_input("Número de CPF do motorista")
            pedido = st.text_input("Número da Nota")
            placa = st.text_input("Placa do veículo")
            data = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")

            submitted = st.form_submit_button("✅ Confirmar Dados")
            if submitted and all ([transportadora,motorista,cpf,pedido,placa]):
                return{
                    "transportadora": transportadora,
                    "motorista": motorista,
                    "cpf": cpf,
                    "pedido":pedido,
                    "placa": placa,
                    "data": data
                }
            elif submitted:
                st.warning("⚠ Preencha todos os campos.")
                return None