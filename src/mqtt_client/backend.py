import time
from config import *
import AWSIoTPythonSDK
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from ..Context.speaker import SoftwareInteligenzaArtificiale
import pyttsx3
from speech_recognition import Recognizer

READ_TOPIC = 'sofia-silent'
WRITE_TOPIC = 'sofia-silent/response'
response_msg = ""
class Device(object):
    '''A class as an interface for any IoT thing which can be registered
    such as sensors actuators etc..   
    these are considered AWS IoT MQTT Clients using TLSv1.2 Mutual Authentication'''

    def __init__(self, client_ID: str):

        self.client: AWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(
            client_ID)
        self.configure_client()

    def configure_client(self):
        self.client.configureEndpoint(END_POINT, 8883)
        self.client.configureCredentials(
            PATH_TO_ROOT_CA, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)
        self.client.connect(keepAliveIntervalSecond=900)

    def publish_data(self, topic: str, payload):
        '''topic format -> thing/measurement/property
        i.e. topic : sensor/temperature/high'''
        self.client.publish(topic, payload, 0)

    def subscribe_to_topic(self, topic: str, custom_callback):
        '''Callback functions should be of the following form
        def callback(client,used_data,message):
            function(message)
        where message has properties message.payload and message.topic'''
        self.client.subscribe(topic, 1, custom_callback)

    def tear_down(self, topic):
        self.client.disconnect()
        self.client.unsubscribe(topic)

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
    except AWSIoTPythonSDK.exception.AWSIoTExceptions.subscribeTimeoutException:
        pass
