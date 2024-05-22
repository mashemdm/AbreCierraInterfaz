import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model
from gtts import gTTS
import os
import playsound

# Configuración de la página
st.set_page_config(page_title="Reconocimiento facial", page_icon="😎")
st.markdown("# Reconocimiento facial")

def on_publish(client, userdata, result):  
    print("El dato ha sido publicado\n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("CollabModeloCamara")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

# Cargar el modelo
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

img_file_buffer = st.camera_input("Toma una Foto")

def play_audio(text):
    tts = gTTS(text=text, lang='es')
    tts.save("temp_audio.mp3")
    try:
        playsound.playsound("temp_audio.mp3")
    except Exception as e:
        print("Error al reproducir el audio:", e)
    finally:
        # Verificar si el archivo existe antes de intentar eliminarlo
        if os.path.exists("temp_audio.mp3"):
            try:
                os.remove("temp_audio.mp3")
            except Exception as e:
                print("Error al eliminar el archivo de audio:", e)

if img_file_buffer is not None:
    # Leer la imagen del buffer
    img = Image.open(img_file_buffer)

    # Redimensionar la imagen
    newsize = (224, 224)
    img = img.resize(newsize)
    img_array = np.array(img)

    # Normalizar la imagen
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    # Ejecutar la inferencia
    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0] > 0.3:
        st.header('Te veo feliz 😁')
        client1.publish("CanalAbreCierra", "{'gesto': 'Feliz'}", qos=0, retain=False)
        play_audio("¡Estoy feliz de verte sonreír!")
    elif prediction[0][1] > 0.3:
        st.header('Te veo triste 😞')
        client1.publish("CanalAbreCierra", "{'gesto': 'Triste'}", qos=0, retain=False)
        play_audio("Lamento verte triste, espero que te sientas mejor pronto.")
    time.sleep(0.2)
