import os
import streamlit as st
from streamlit_bokeh_events import streamlit_bokeh_events
import time
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

# Configuración de la página de Streamlit
st.set_page_config(page_title="Reconocimiento de voz", page_icon="🔊")
st.markdown("# Reconocimiento de voz")
st.sidebar.header("Reconocimiento de voz")

# Función callback para la publicación de mensajes
def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")
    pass

# Función callback para la recepción de mensajes
def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Configuración del broker MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client2 = paho.Client("APPVOZ")
client2.on_message = on_message
client2.on_publish = on_publish
client2.connect(broker, port)
client2.loop_start()

st.write("Toca el botón y dime cómo te sientes")

# Botón de Streamlit
if st.button("Dame click"):
    st.write("Reconocimiento de voz iniciado...")

    # Código JavaScript para el reconocimiento de voz
    stt_js = """
    <script>
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    </script>
    """
    st.components.v1.html(stt_js)

    result = streamlit_bokeh_events(
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0
    )

    if result:
        if "GET_TEXT" in result:
            st.write(result.get("GET_TEXT"))
            message = json.dumps({"gesto": result.get("GET_TEXT").strip()})
            ret = client2.publish("CanalAbreCierra", message)

# Mantener la conexión MQTT activa
client2.loop_stop()
client2.disconnect()
