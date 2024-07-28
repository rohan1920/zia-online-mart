from flask import Flask
from kafka import KafkaConsumer
import json
import threading

app = Flask(__name__)
consumer = KafkaConsumer('order_topic', bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

def consume():
    for message in consumer:
        order = message.value
        print(f"Notification: New order received - {order}")

threading.Thread(target=consume).start()

if __name__ == '__main__':
    app.run(port=5004)
