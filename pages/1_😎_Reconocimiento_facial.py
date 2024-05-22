import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model
import os
import glob
from gtts import gTTS

if os.path.exists('keras_model.h5'):
    print("The file 'keras_model.h5' exists in the current working directory.")
else:
    print("The file 'keras_model.h5' does not exist in the current working directory.")

st.set_page_config(page_title="Reconocimiento facial", page_icon="😎")
st.markdown("# Reconocimiento facial")

try:
    os.mkdir("temp")
except FileExistsError:
    pass

def on_publish(client, userdata, result):             #create function for callback
    print("el dato ha sido publicado \n")
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

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("Cerradura Inteligente")

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    img = Image.open(img_file_buffer)
    newsize = (224, 224)
    img = img.resize(newsize)
    img_array = np.array(img)
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0] > 0.3:
        st.header('Te veo feliz 😁')
        client1.publish("CanalAbreCierra", "{'gesto': 'Feliz'}", qos=0, retain=False)
        time.sleep(0.2)
    if prediction[0][1] > 0.3:
        st.header('Te veo triste ☹️')
        result, output_text = text_to_speech("Te veo triste", "es")
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.markdown(f"## Texto en audio:")
        st.write(f"{output_text}")
        client1.publish("CanalAbreCierra", "{'gesto': 'Triste'}", qos=0, retain=False)
        time.sleep(0.2)

text = "Me encanta verte feliz, cómo puedo ayudarte"
tld = "es"

def text_to_speech(text, tld):
    tts = gTTS(text, lang=tld, slow=False)
    try:
        my_file_name = text[:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
