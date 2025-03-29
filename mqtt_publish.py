import paho.mqtt.client as mqtt
import ssl

broker = "set-p-get-01-mqtt.bm.icts.kuleuven.be"  
topic = "test/topic"

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} from topic {msg.topic}")


client = mqtt.Client("Subscriber")


client.tls_set(certfile="path/to/cert.pem", keyfile="path/to/key.pem", tls_version=ssl.PROTOCOL_TLSv1_2)


client.connect(broker, 8883)

client.subscribe(topic)

client.loop_forever()

