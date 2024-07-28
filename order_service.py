from flask import Flask, request, jsonify
from kafka import KafkaConsumer, KafkaProducer
import json
import threading

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = KafkaConsumer('product_topic', bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

orders = []

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    orders.append(data)
    producer.send('order_topic', data)
    return jsonify(data), 201

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    return jsonify(order) if order else ('', 404)

if __name__ == '__main__':
    app.run(port=5003)
