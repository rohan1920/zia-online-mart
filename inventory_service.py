from flask import Flask, request, jsonify
from kafka import KafkaConsumer, KafkaProducer
import json
import threading

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = KafkaConsumer('product_topic', bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

inventory = {}

def consume():
    for message in consumer:
        product = message.value
        inventory[product['id']] = 100  # Initial inventory level

threading.Thread(target=consume).start()

@app.route('/inventory/<product_id>', methods=['GET'])
def get_inventory(product_id):
    stock = inventory.get(product_id)
    return jsonify({'product_id': product_id, 'stock': stock}) if stock is not None else ('', 404)

if __name__ == '__main__':
    app.run(port=5002)
