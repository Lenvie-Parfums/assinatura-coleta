from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from PIL import Image
import io
import os
import re

class GeradorPDF:
    def __init__(self, dados, assinatura_array,logo_path="img/logolenvie.png"):
        self.dados = dados
        self.assinatura = Image.fromarray(assinatura_array.astype("uint8"))
        self.logo_path = logo_path

    def gerar_pdf(self):
        buffer = io.BytesIO()
        largura, altura = A4
        c = canvas.Canvas(buffer, pagesize=A4)

        # === Logo centralizado ===
        if os.path.exists(self.logo_path):
            logo_width = 40 * mm
            logo_height = 20 * mm
            c.drawImage(
                self.logo_path,
                (largura - logo_width) / 2,
                altura - 100,
                width=logo_width,
                height=logo_height,
                mask="auto"
            )

       # === Título ===
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(largura / 2, altura - 140, "📄 Comprovante de Retirada")

        # === Linha separadora ===
        c.setLineWidth(1)
        c.line(40, altura - 110, largura - 40, altura - 110)

        # === Linha separadora ===
        y = altura -180
        espacamento = 20

        pedidos = [p.strip() for p in re.split(r"[,\\-]", self.dados['pedido']) if p.strip()]

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Transportadora: {self.dados['transportadora']}")
        c.drawString(50, y-espacamento, f"Motorista: {self.dados['motorista']}")
        c.drawString(50, y - 2*espacamento, f"CPF:{self.dados['cpf']}")

        for i in range(0,len(pedidos),5):
            bloco = pedidos[i:i+5]
            linha = " | ".join(n.strip() for n in bloco)
            if i == 0:  # primeira linha
                c.drawString(50, y - 3*espacamento, f"Número da Nota: {linha}")
            else:  # linhas seguintes
                c.drawString(145, y - (3 + i//5)*espacamento, linha)  # desloca um pouco pra alinhar

        c.drawString(50, y - (4 + len(pedidos)//5) * espacamento, f"Placa do veículo: {self.dados['placa']}")
        c.drawString(50, y - (5 + len(pedidos)//5) * espacamento, f"Data da Retirada: {self.dados['data']}")

        assinatura_path = "assinatura_temp.png"
        self.assinatura.save(assinatura_path)
        c.drawImage(assinatura_path, 50, y - (9 + len(pedidos)//5) * espacamento, width=200, height=60)
        c.drawString(50, y - (10 + len(pedidos)//5) * espacamento, "Assinatura")

        c.save()
        buffer.seek(0)
        return buffer
