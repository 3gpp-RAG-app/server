import time
from flask import Blueprint, request, jsonify, Response
from app.controllers.milvus_controller import search
from app import app 



from flask import Blueprint, request, jsonify
from app.controllers.milvus_controller import search

milvus_bp = Blueprint('milvus', __name__)

@milvus_bp.route('/search', methods=['POST'])
def milvus_search():
    query = request.get_json()
    if not query:
        return jsonify({"error": "Query parameter not provided"}), 400

    results = search(query)
    return jsonify({"results": results})



def generate_data():
    data = [
        {"id": 1, "status": "This test db is runing"},

    ]

    for item in data:
        yield f"Data: {item}\n"
        time.sleep(1)

@app.route('/streaming_data')
def streaming_data():
    return Response(generate_data(), content_type='text/plain', status=200)
