from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

products = {}

@app.route('/product', methods=['POST'])
def add_product():
    data = request.json
    product_id = data['id']
    products[product_id] = data
    producer.send('product_topic', data)
    return jsonify(data), 201

@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    return jsonify(product) if product else ('', 404)

if __name__ == '__main__':
    app.run(port=5001)
