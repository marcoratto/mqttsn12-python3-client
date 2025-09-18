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
import time
import sys
import logging

from mqttsn12.MqttSnConstants import MqttSnConstants
from mqttsn12.client.MqttSnClient import MqttSnClient, MqttSnListener
from mqttsn12.client.MqttSnClientException import MqttSnClientException
from mqttsn12.packets import *

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MQTT_SN_HOST = "127.0.0.1"
MQTT_SN_PORT = 2442

actual = ""

class MyListener(MqttSnListener):
    def message_arrived(self, topic_id: int, topic_name: str, data: bytes) -> None:
        print(f"Messaggio ricevuto su {topic_name} (ID={topic_id}): {data.decode()}")
        actual = data.decode()

mqttsn_client = MqttSnClient()
mqttsn_client.open(MQTT_SN_HOST, MQTT_SN_PORT)

mqttsn_client.send_connect()

mylistener = MyListener()

mqttsn_client.send_subscribe("mqttsn/sample/sub", MqttSnConstants.QOS_1, mylistener)

expected = "Hello World from MQTT"

try:
	keep_running = True
	while keep_running:
		mqttsn_client.polling()
		if (actual == expected):
			keep_running = False
	
	mqttsn_client.send_disconnect(0)

except MqttSnClientException as e:
	print(e)

mqttsn_client.close()
