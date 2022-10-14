import time
from Context.speaker import SoftwareInteligenzaArtificiale
import pyttsx3
from speech_recognition import Recognizer
from device import Device
import AWSIoTPythonSDK 

READ_TOPIC = 'sofia-silent'
WRITE_TOPIC = 'sofia-silent/response'
response_msg = ""

def callback(client,used_data,message):
    global response_msg

    msg = message.payload.decode()
    print(msg)
    print(type(msg))
    audio_engine = SoftwareInteligenzaArtificiale()
    audio_engine.run_context(msg)
    

    if msg == "listen":
        listener = Recognizer()
        audio_engine = SoftwareInteligenzaArtificiale()
        engine = pyttsx3.init()
        
        engine.say('      I am listening')
        engine.runAndWait()
        audio_engine.start_listening(listener, engine)
        response_msg = "command executed successfully ✅"

device_read = Device("readID")
device_write = Device("writeID")
device_read.subscribe_to_topic(READ_TOPIC,callback)
while True:
    try:
        if response_msg == "":
            print("waiting for a command... 🤖")
        else:
            device_write.publish_data(WRITE_TOPIC,response_msg)
        time.sleep(2)
    except:
        pass
