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
import unittest
import random
import logging
from logging.handlers import TimedRotatingFileHandler
import paho.mqtt.client as mqtt

from mqttsn12.MqttSnConstants import MqttSnConstants
from mqttsn12.client.MqttSnClient import MqttSnClient
from mqttsn12.client.MqttSnClientException import MqttSnClientException
from mqttsn12.packets import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

class UnitTest(unittest.TestCase):
    MQTT_SN_HOST = "127.0.0.1"
    MQTT_SN_PORT = 2442
    MQTT_ID = "python"
    MQTT_HOST = "127.0.0.1"
    MQTT_PORT = 1883
    MQTT_QOS = 1
    MQTT_USER = "python"
    MQTT_PASS = "python"
    MQTT_CLEAN_SESSION = False
    
    def setUp(self):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id= self.MQTT_ID, clean_session= self.MQTT_CLEAN_SESSION) 
        self.mqttc.username_pw_set(username= self.MQTT_USER, password= self.MQTT_PASS)

        self.mqttsn_client = MqttSnClient()

    def tearDown(self):
        self.mqttsn_client.close()

    def test_custom_client_id(self):
        print("test_pub_qos0")
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.set_client_id("test_custom_client_id")
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_publish("mqttsn/test/custom_client_id", 
                        "test_custom_client_id", 
                        MqttSnConstants.QOS_0, 
                        False);

        time.sleep(1)

        self.mqttsn_client.send_disconnect(0)
        
    def test_pub_qos0(self):
        print("test_pub_qos0")
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_publish("mqttsn/test/pub_qos0", 
                        "test_pub_qos0", 
                        MqttSnConstants.QOS_0, 
                        False);

        time.sleep(1)

        self.mqttsn_client.send_disconnect(0)

    def test_pub_qos0_retained(self):
        print("test_pub_qos0_retained")
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_publish("mqttsn/test/pub_qos0_retained", 
                        "test_pub_qos0_retained", 
                        MqttSnConstants.QOS_0, 
                        True);

        time.sleep(1)

        self.mqttsn_client.send_disconnect(0)
        
    def test_pub_qos1(self):
        print("test_pub_qos1")
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_publish("mqttsn/test/pub_qos1", 
                        "test_pub_qos1", 
                        MqttSnConstants.QOS_1, 
                        False);

        time.sleep(1)

        self.mqttsn_client.send_disconnect(0)

#
#Note:
#On Mac OSX:
#sysctl net.inet.udp.maxdgram
#net.inet.udp.maxdgram: 9216
#sudo sysctl -w net.inet.udp.maxdgram=65535
#
    def test_pub_big_payload_qos1(self):
        print("test_pub_big_payload_qos1")
        
        parts = []
        for _ in range(5000):
            parts.append("Hello " + str(random.randint(0, 0xFFFF)))

        payload = ''.join(parts)

        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_publish("mqttsn/test/pub_big_payload_qos1", 
                        payload, 
                        MqttSnConstants.QOS_1, 
                        False);

        time.sleep(1)

        self.mqttsn_client.send_disconnect(0)

    def test_pub_qos1_retained(self):
        print("test_pub_qos1_retained")
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_publish("mqttsn/test/pub_qos1_retained", 
                        "test_pub_qos1_retained", 
                        MqttSnConstants.QOS_1, 
                        True);

        time.sleep(1)

        self.mqttsn_client.send_disconnect(0)

    def test_pub_qos3(self):
        print("test_pub_qos3")
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_publish_with_bytes("RM".encode(), 
                        "test_pub_qos3", 
                        MqttSnConstants.QOS_N1, 
                        False);

    def test_pub_predefined(self):
        print("test_pub_predefined")
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        
        # 1 -> mqttsn/test/predefined_pub
        self.mqttsn_client.send_publish_predefined(1, 
                        "test_pub_predefined", 
                        MqttSnConstants.QOS_N1, 
                        False);

    def test_pub_predefined_retained(self):
        print("test_pub_predefined")
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        
        # 2 -> mqttsn/test/predefined_retained
        self.mqttsn_client.send_publish_predefined(2, 
                        "test_pub_predefined_retained", 
                        MqttSnConstants.QOS_N1, 
                        True);
                        
if __name__ == '__main__':
    unittest.main()
