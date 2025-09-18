# mqttsn12-python3-client
Python3 Client implementation of the Protocol MQTT-SN 1.2 (https://mqtt.org/mqtt-specification/ or https://groups.oasis-open.org/higherlogic/ws/public/document?document_id=66091).

The library was tested with EMQX (https://www.emqx.com/en) and Hive MQ Edge (https://www.hivemq.com/products/hivemq-edge/).

Start from this url http://www.steves-internet-guide.com/mqtt-sn/ for understanding more about the protocol MQTT-SN.

Below you can find the code coverage:
| Name                                         |    Stmts |     Miss |   Cover |
|--------------------------------------------- | -------: | -------: | ------: |
| src/mqttsn12/MqttSnConstants.py              |       61 |        0 |    100% |
| src/mqttsn12/\_\_init\_\_.py                 |        0 |        0 |    100% |
| src/mqttsn12/client/MqttSnClient.py          |      623 |      132 |     79% |
| src/mqttsn12/client/MqttSnClientException.py |       12 |        8 |     33% |
| src/mqttsn12/client/\_\_init\_\_.py          |        0 |        0 |    100% |
| src/mqttsn12/packets.py                      |      857 |      273 |     68% |
| tests/unit\_test\_publisher.py               |      110 |        1 |     99% |
| tests/unit\_test\_subscriber.py              |      236 |       17 |     93% |
|                                    **TOTAL** | **1899** |  **431** | **77%** |

Below you can find the list of the Message Type implemented:

|MsgType|Field|Status|Note|
|-|-|-|-|
|0x00|ADVERTISE|NA||
|0x01|SEARCHGW|Implemented||
|0x02|GWINFO|Implemented||
|0x03|reserved|NA||
|0x04|CONNECT|Implemented||
|0x05|CONNACK|Implemented||
|0x06|WILLTOPICREQ|Implemented||
|0x07|WILLTOPIC|Implemented||
|0x08|WILLMSGREQ|Implemented||
|0x09|WILLMSG|Implemented||
|0x0A|REGISTER|Implemented||
|0x0B|REGACK|Implemented||
|0x0C|PUBLISH|Implemented||
|0x0D|PUBACK|Implemented||
|0x0E|PUBCOMP|NA||
|0x0F|PUBREC|NA||
|0x10|PUBREL|NA||
|0x11|reserved|NA||
|0x12|SUBSCRIBE|Implemented||
|0x13|SUBACK|Implemented||
|0x14|UNSUBSCRIBE|Implemented||
|0x15|UNSUBACK|Implemented||
|0x16|PINGREQ|Implemented||
|0x17|PINGRESP|Implemented||
|0x18|DISCONNECT|Implemented||
|0x19|reserved|NA||
|0x1A|WILLTOPICUPD|Implemented||
|0x1B|WILLTOPICRESP|Implemented||
|0x1C|WILLMSGUPD|Implemented||
|0x1D|WILLMSGRESP|Implemented||
|0x1E-0xFD|reserved|NA||
|0xFE|Encapsulated message|NA||
|0xFF|reserved|NA||
