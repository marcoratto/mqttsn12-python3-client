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
from mqttsn12.client.MqttSnClient import MqttSnClient, MqttSnListener
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

actual = None
keep_running = True

class MyListener(MqttSnListener):
    def message_arrived(self, topic_id: int, topic_name: str, data: bytes) -> None:
        global actual
        global keep_running
        actual = data.decode("utf-8")
        print(f"Messaggio ricevuto su {topic_name} (ID={topic_id}): {actual}")
        keep_running = False

class TestSubscriber(unittest.TestCase):
    MQTT_SN_HOST = "127.0.0.1"
    MQTT_SN_PORT = 2442
    MQTT_ID = "python"
    MQTT_HOST = "127.0.0.1"
    MQTT_PORT = 1883
    MQTT_QOS = 1
    MQTT_USER = None
    MQTT_PASS = None
    MQTT_CLEAN_SESSION = False

    def on_log(self, mqttc, obj, level, string):
        print(string)
        
    def setUp(self):
        global actual
        global keep_running

        actual = None
        keep_running = True
        
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id= self.MQTT_ID, clean_session= self.MQTT_CLEAN_SESSION) 
        if self.MQTT_USER is not None and self.MQTT_PASS is not None:
            self.mqttc.username_pw_set(username= self.MQTT_USER, password= self.MQTT_PASS)

        self.mqttc.on_log = self.on_log
        
        self.mqttc.connect(self.MQTT_HOST, int(self.MQTT_PORT), 60)

        self.mqttsn_client = MqttSnClient()
        self.mqttsn_client.set_timeout(60)

    def test_unsubcribe_normal_topic(self):
        global keep_running
        global actual
        print("test_unsubcribe_normal_topic")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("mqttsn/test/unsubcribe_normal_topic", 
                        MqttSnConstants.QOS_0, 
                        myListener)

        time.sleep(1)
                        
        self.mqttsn_client.send_unsubscribe("mqttsn/test/unsubcribe_normal_topic")
            
        self.mqttsn_client.send_disconnect(0)

    def test_unsubcribe_short_topic(self):
        global keep_running
        global actual
        print("test_unsubcribe_short_topic")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("AA", 
                        MqttSnConstants.QOS_0, 
                        myListener)

        time.sleep(1)
                        
        self.mqttsn_client.send_unsubscribe("AA")
            
        self.mqttsn_client.send_disconnect(0)

    def test_unsubcribe_predefined_topic(self):
        global keep_running
        global actual
        print("test_unsubcribe_predefined_topic")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe_predefined(2, 
                        MqttSnConstants.QOS_N1, 
                        myListener)

        time.sleep(1)
                        
        self.mqttsn_client.send_unsubscribe_predefined(2)
            
        self.mqttsn_client.send_disconnect(0)
                        
    def tearDown(self):
        self.mqttsn_client.close()
      
    def test_sub_qos0(self):
        global keep_running
        global actual
        print("test_sub_qos0")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("mqttsn/test/sub_qos0", 
                        MqttSnConstants.QOS_0, 
                        myListener)

        self.mqttc.loop_start()

        expected = "test_sub_qos0"

        self.mqttc.publish("mqttsn/test/sub_qos0", expected, qos=0, retain=False)
        self.mqttc.disconnect()
        self.mqttc.loop_stop()

        try:
            while keep_running:
                self.mqttsn_client.polling()
                time.sleep(0.1)

        except MqttSnClientException as e:
            print(e)
            
        self.mqttsn_client.send_disconnect(0)

        assert actual == expected, f"actual={actual!r} non corrisponde"

    def test_sub_qos1(self):
        global keep_running
        global actual
        print("test_sub_qos1")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("mqttsn/test/sub_qos1", 
                        MqttSnConstants.QOS_1, 
                        myListener)

        self.mqttc.loop_start()

        expected = "test_sub_qos1"

        self.mqttc.publish("mqttsn/test/sub_qos1", expected, qos=1, retain=False)
        self.mqttc.disconnect()
        self.mqttc.loop_stop()

        try:
            while keep_running:
                self.mqttsn_client.polling()
                time.sleep(0.1)

        except MqttSnClientException as e:
            print(e)
            
        self.mqttsn_client.send_disconnect(0)

        assert actual == expected, f"actual={actual!r} non corrisponde"

    def test_sub_lwt(self):
        global keep_running
        global actual
        print("test_sub_lwt")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.set_will("mqttsn/lwt/status", "offline_ko", MqttSnConstants.QOS_1, True)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("mqttsn/test/sub_lwt", 
                        MqttSnConstants.QOS_1, 
                        myListener)

        self.mqttc.loop_start()

        expected = "test_sub_lwt"

        self.mqttc.publish("mqttsn/test/sub_lwt", expected, qos=1, retain=False)
        self.mqttc.disconnect()
        self.mqttc.loop_stop()

        try:
            while keep_running:
                self.mqttsn_client.polling()
                time.sleep(0.1)

        except MqttSnClientException as e:
            print(e)
            
        self.mqttsn_client.send_disconnect(0)

        assert actual == expected, f"actual={actual!r} non corrisponde"
                                
    def test_sub_big_payload(self):
        global keep_running
        global actual
        print("test_sub_big_payload")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("mqttsn/test/sub_big_payload", 
                        MqttSnConstants.QOS_1, 
                        myListener)

        self.mqttc.loop_start()

        parts = []
        for _ in range(100):
            parts.append("sub_big_payload " + str(random.randint(0, 0xFFFF)))

        expected = ''.join(parts)

        self.mqttc.publish("mqttsn/test/sub_big_payload", expected, qos=1, retain=False)
        self.mqttc.disconnect()
        self.mqttc.loop_stop()

        try:
            while keep_running:
                self.mqttsn_client.polling()
                time.sleep(0.1)

        except MqttSnClientException as e:
            print(e)
            
        self.mqttsn_client.send_disconnect(0)

        assert actual == expected, f"actual={actual!r} non corrisponde"

    def test_sub_predefined_sub(self):
        global keep_running
        global actual
        print("test_sub_predefined_sub")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe_predefined(2, 
                        MqttSnConstants.QOS_N1, 
                        myListener)

        self.mqttc.loop_start()

        expected = "test_sub_predefined_sub"

        self.mqttc.publish("mqttsn/test/predefined_sub", expected, qos=0, retain=False)
        self.mqttc.disconnect()
        self.mqttc.loop_stop()

        try:
            while keep_running:
                self.mqttsn_client.polling()
                time.sleep(0.1)

        except MqttSnClientException as e:
            print(e)
            
        self.mqttsn_client.send_disconnect(0)

        assert actual == expected, f"actual={actual!r} non corrisponde"

    def test_sub_short_topic(self):
        global keep_running
        global actual
        print("test_sub_short_topic")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("RM", 
                        MqttSnConstants.QOS_1, 
                        myListener)

        self.mqttc.loop_start()

        expected = "test_sub_short_topic"

        self.mqttc.publish("RM", expected, qos=0, retain=False)
        self.mqttc.disconnect()
        self.mqttc.loop_stop()

        try:
            while keep_running:
                self.mqttsn_client.polling()
                time.sleep(0.1)

        except MqttSnClientException as e:
            print(e)
            
        self.mqttsn_client.send_disconnect(0)

        assert actual == expected, f"actual={actual!r} non corrisponde"

    def test_will_message_update(self):
        global keep_running
        global actual
        print("test_will_message_update")

        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.set_will("mqttsn/lwt/status", "offline_ko", MqttSnConstants.QOS_0, True)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_will_message_update("off_ko")
        time.sleep(3)

    def test_lwt_2(self):
        global keep_running
        global actual
        print("test_lwt_2")

        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.set_will_message("offline_ko")
        self.mqttsn_client.set_will_qos(MqttSnConstants.QOS_0)
        self.mqttsn_client.set_will_retain(True)
        self.mqttsn_client.set_will_topic("mqttsn/lwt/status")
        self.mqttsn_client.send_connect()
        time.sleep(3)

    def test_update_lwt_topic(self):
        global keep_running
        global actual
        print("test_update_lwt_topic")
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.set_will("mqttsn/lwt/status", "offline_ko", MqttSnConstants.QOS_0, True)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_will_topic_update("mqttsn/lwt/state")
        time.sleep(3)
        #self.mqttc.disconnect()

    def test_ping(self):
        global keep_running
        global actual
        print("test_ping")
        
        keepalive = 5
        
        myListener = MyListener()
        
        self.mqttsn_client.set_keep_alive(keepalive)
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("mqttsn/test/ping", 
                        MqttSnConstants.QOS_0, 
                        myListener)

        self.mqttc.loop_start()
        
        expected = "test_ping"
        start = time.time()
        published = False
    
        try:
            while keep_running:
                self.mqttsn_client.polling()
                time.sleep(1)
                elapsed = time.time() - start
                
                # quando è passato almeno un intervallo di keepalive,
                # presupponiamo che ci sia stato lo scambio PINGREQ/PINGRESP
                if not published and elapsed > keepalive+1:
                    published = True                
                    self.mqttc.publish("mqttsn/test/ping", expected, qos=0, retain=False)
                
        except MqttSnClientException as e:
            print(e)
            
        self.mqttc.disconnect()
        self.mqttc.loop_stop()
        self.mqttsn_client.send_disconnect(0)

        assert actual == expected, f"actual={actual!r} non corrisponde"

    def test_sub_wildcard_hash(self):
        global keep_running
        global actual
        print("test_sub_wildcard_hash")
        
        myListener = MyListener()
        
        self.mqttsn_client.open(self.MQTT_SN_HOST, self.MQTT_SN_PORT)
        self.mqttsn_client.send_connect()
        self.mqttsn_client.send_subscribe("mqttsn/test/sub/wildcard_hash/#", 
                        MqttSnConstants.QOS_0, 
                        myListener)

        actual = None
        expected = "test_sub_wildcard_hash_0"
        self.mqttc.loop_start()
        self.mqttc.publish("mqttsn/test/sub/wildcard_hash/0", expected, qos=1, retain=False)
        
        self.mqttsn_client.polling()
        
        self.mqttc.publish("mqttsn/test/sub/wildcard_hash/0", expected, qos=1, retain=False)        
        try:
            while actual is None:
                self.mqttsn_client.polling()
                time.sleep(0.1)

        except MqttSnClientException as e:
            print(e)
        assert actual == expected, f"actual={actual!r} non corrisponde"

        actual = None
        expected = "test_sub_wildcard_hash_1"
        self.mqttc.publish("mqttsn/test/sub/wildcard_hash/1", expected, qos=1, retain=False)
        
        self.mqttsn_client.polling()
        
        self.mqttc.publish("mqttsn/test/sub/wildcard_hash/1", expected, qos=1, retain=False)
        try:
            while actual is None:
                self.mqttsn_client.polling()
                time.sleep(0.1)

        except MqttSnClientException as e:
            print(e)                   
        assert actual == expected, f"actual={actual!r} non corrisponde"
                    
        time.sleep(1)
                    
        self.mqttsn_client.send_disconnect(0)
        self.mqttc.disconnect()
        self.mqttc.loop_stop()
                                                        
if __name__ == '__main__':
    unittest.main()
