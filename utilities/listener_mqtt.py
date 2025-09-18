#!/usr/bin/env python3
# MIT License
# 
# Copyright (c) 2025 Marco Ratto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import sys
import time
from pathlib import Path

# pip3 install paho-mqtt
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

# MQTT Settings 
MQTT_ID = os.getlogin() + "@" + os.path.basename(__file__)
MQTT_USER = "python"
MQTT_PASS = "python"

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEP_ALIVE = 60
MQTT_QOS = 1
MQTT_CLEAN_SESSION = False

MQTT_LWT_TOPIC = "status/" + MQTT_ID
MQTT_LWT_QOS = 1
MQTT_LWT_RETAIN = True
MQTT_LWT_MSG_OFFLINE_OK = 'offline_ok'
MQTT_LWT_MSG_OFFLINE_KO = 'offline_ko'
MQTT_LWT_MSG_ONLINE = 'online'

# Stato della connessione
connected = False  
reconnect_attempts = 0 

def reconnect(client):
    """ Prova a riconnettersi con un ritardo esponenziale """
    global reconnect_attempts
    while not connected:
        try:
            reconnect_attempts += 1
            wait_time = min(2 ** reconnect_attempts, 60)  # Backoff esponenziale max 60 sec
            print(f"Tentativo {reconnect_attempts} di riconnessione in {wait_time} secondi...")
            time.sleep(wait_time)

            print("Tentativo di riconnessione inviato...")
            client.reconnect()
            return  # Esce se la riconnessione ha successo
        except Exception as e:
            print(f"Errore nella riconnessione: {e}")
            
def on_disconnect(client, userdata, flags, reason_code, properties):
    global connected, reconnect_attempts, ret_code
    
    print(f"Disconnected, reason code: {reason_code}")
    connected = False
    print("Disconnesso dal broker!")
    if ret_code != 99:
        print("Connessione persa! Tentativo di riconnessione...")
        reconnect(client)

def on_connect(client, userdata, flags, rc, properties):
    global connected, reconnect_attempts
    if rc == 0:
        client.connected_flag = True #set flag
        connected = True
        reconnect_attempts = 0  # Reset dei tentativi di riconnessione
        print("connected OK")
        mqttc.publish(MQTT_LWT_TOPIC, MQTT_LWT_MSG_ONLINE, qos=MQTT_LWT_QOS, retain=MQTT_LWT_RETAIN)
        mqtt_topics = [('mqttsn/#', MQTT_QOS), ('RM', MQTT_QOS)]
        for topic in mqtt_topics:
            print("Subscribe to topic '" + topic[0] + "' with QOS=" + str(topic[1]))
            client.subscribe(topic)
    else:
        print("Bad connection Returned code=",rc)

def on_message(mqttc, obj, msg):
    try:
        now = datetime.now().isoformat()  
        print("***********************************")
        print(f"now: {now}")
        print(f"Topic: {msg.topic}")
        print(f"QoS: {msg.qos}")
        print(f"Retained: {msg.retain}")
        print(f"Message ID: {msg.mid}")
        payload = msg.payload
        print("Payload: " + payload.hex())
            
    except UnicodeDecodeError:
        print("Errore di decodifica del payload")
    except Exception as e:
        print(f"Errore durante l'elaborazione del messaggio: {e}")

def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))

def on_log(mqttc, obj, level, string):
    print(string)

print("Connecting to Broker with ClientID: " + MQTT_ID)           
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id= MQTT_ID, clean_session= MQTT_CLEAN_SESSION) 

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe
#mqttc.on_log = on_log

mqttc.will_set(MQTT_LWT_TOPIC, payload=MQTT_LWT_MSG_OFFLINE_KO, qos=MQTT_LWT_QOS, retain=MQTT_LWT_RETAIN)

mqttc.username_pw_set(username= MQTT_USER, password= MQTT_PASS)

# Connect
mqttc.connect(MQTT_BROKER, int(MQTT_PORT), int(MQTT_KEEP_ALIVE))

# Continue the network loop
ret_code = 0
try:
    mqttc.loop_forever()
        
except KeyboardInterrupt:
    ret_code = 99
    
print("Chiusura del client MQTT...")
mqttc.publish(MQTT_LWT_TOPIC, MQTT_LWT_MSG_OFFLINE_OK, qos=MQTT_LWT_QOS, retain=MQTT_LWT_RETAIN)
time.sleep(1)
mqttc.disconnect()
    
sys.exit(ret_code)
