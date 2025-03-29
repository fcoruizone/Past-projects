import paho.mqtt.client as mqtt
import ssl

# Broker details
broker = "set-p-get-01-mqtt.bm.icts.kuleuven.be"  # Replace with your broker address
topic = "test/topic"

# Callback function when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} from topic {msg.topic}")

# Create MQTT client
client = mqtt.Client("Subscriber")

# Set up the TLS context for secure connection
client.tls_set(certfile="path/to/cert.pem", keyfile="path/to/key.pem", tls_version=ssl.PROTOCOL_TLSv1_2)

# Connect to the broker securely (using port 8883 for TLS)
client.connect(broker, 8883)

# Subscribe to the topic
client.subscribe(topic)

# Start the loop to receive messages
client.loop_forever()

