import streamlit as st

st.set_page_config(
    page_title="Inicio",
    page_icon="👋",
)

st.write("# Bienvenido al lector de emociones! 👋")

st.sidebar.success("Selecciona la opción de lectura.")

st.markdown(
    """
    La aplicación **"Lector de emociones"** utiliza la cámara del dispositivo para detectar las emociones básicas (tristeza y felicidad) en el rostro del usuario.
    A partir de este reconocimiento, un robot asociado imita la expresión facial detectada y enciende un foco de un color específico de acuerdo a la emoción.

    
    **👈 Esccoge el metodo para reconocer tu emoción** 
    ### Qué usos puede tener esta interfaz?
    - **Autoevaluación emocional:** Permite a los usuarios monitorear sus propias emociones y desarrollar estrategias para gestionarlas de manera efectiva.
    - **Fomentar la inteligencia emocional en niños:** Brinda una forma interactiva y divertida de aprender a reconocer y expresar emociones.
    - **Evaluar la satisfacción del cliente:** Medir el nivel de satisfacción de los clientes en tiempo real y mejorar la calidad del servicio.

"""
)
