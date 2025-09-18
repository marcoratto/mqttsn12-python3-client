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
from mqttsn12.client.MqttSnClient import MqttSnClient
from mqttsn12.client.MqttSnClientException import MqttSnClientException
from mqttsn12.packets import *

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MQTT_SN_HOST = "127.0.0.1"
MQTT_SN_PORT = 2442

mqttsn_client = MqttSnClient()
#mqttsn_client.set_client_id("sample_pub")
mqttsn_client.open(MQTT_SN_HOST, MQTT_SN_PORT)

mqttsn_client.send_connect()

mqttsn_client.send_publish("mqttsn/sample", 
				"Hello World from Python 3!", 
				MqttSnConstants.QOS_1, 
				False);

time.sleep(1)

mqttsn_client.send_disconnect(0)

mqttsn_client.close()
