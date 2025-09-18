#!/bin/bash
mosquitto_pub -h 127.0.0.1 -p 1883 -q 1 -t "mqttsn/sample/sub" -m "Hello World from MQTT" -q 1 -u python -P python
