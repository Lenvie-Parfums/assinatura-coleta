import requests
import json
import time
import streamlit as st

APP_KEY = st.secrets["APP_KEY"]
APP_SECRET = st.secrets["APP_SECRET"]

def ConsultarNF(numeroNF):
    endpoint = "https://app.omie.com.br/api/v1/produtos/nfconsultar/"
    payload ={
        "call": "ConsultarNF",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [
            {
                "tpNF":1,
                "nNF":numeroNF
            }
        ]
    }

    try:
        response = requests.post(endpoint,json=payload, timeout=15)
        response.raise_for_status()

        resultado = response.json()
        #print("===== RETORNO DA API =====")
        #print(json.dumps(resultado, indent=2, ensure_ascii=False))
        #print("===========================")

        if "faultstring" in resultado:
            raise Exception(f"Erro API Omie {resultado['faultstring']}")

        idPedido = resultado.get("compl", {}).get("nIdPedido")

        if not idPedido:
            raise ValueError(f"Nota {numeroNF} não retornou o ID do pedido!")

        print (f"Código do Pedido: {idPedido}")

        time.sleep(0.5)

        sucessso = TrocarEtapa(idPedido)

        if not sucessso:
            raise Exception(f"Falha ao trocar etapa do pedido{idPedido}")
        return True

    except Exception as e:
        print ("Erro em consultarNF:")
        print(e)
        return False  # devolve erro
    
def TrocarEtapa(idPedido):
    endpointEtapa = "https://app.omie.com.br/api/v1/produtos/pedido/"
    payload={
        "call":"TrocarEtapaPedido",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param":[
            {
                "codigo_pedido": idPedido,
                "etapa":"70"
            }
        ]
    }

    try:
        responseEtapa = requests.post(endpointEtapa,json=payload, timeout=15)
        responseEtapa. raise_for_status()

        resultadoEtapa = responseEtapa.json()

        if "faulstring" in resultadoEtapa:
            raise Exception(f"Erro API Omie:{resultadoEtapa['faultstring']}")

        print("===== RETORNO DA API =====")
        print(json.dumps(resultadoEtapa, indent=2, ensure_ascii=False))
        print("===========================")

        print ("Etapa alterado com sucesso:", idPedido)
        return True

    except Exception as e:
        print(f"Erro na consulta:{idPedido}")
        print(e)
        return False

##if __name__ == "__main__":
##    ConsultarNF(32195)