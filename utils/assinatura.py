from streamlit_drawable_canvas import st_canvas
import streamlit as st
import numpy as np

class AssinaturaCanvas:
    def capturar_assinatura(self):
        st.write("✍️ Assinatura do motorista:")
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0.05)",
            stroke_width=2,
            stroke_color="#000000",
            background_color="#ffffff",
            height=300,
            width=800,
            drawing_mode="freedraw",
            key="canvas_assinatura"
        )
        if canvas_result.image_data is not None:
            img_array = np.array(canvas_result.image_data, dtype="uint8")
            return img_array
        return None