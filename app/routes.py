import time
from flask import Blueprint, request, jsonify, Response
from app.controllers.milvus_controller import search
from app.models import Conversation
from datetime import datetime
from .models import db

milvus_bp = Blueprint('milvus', __name__)


@milvus_bp.route('/search', methods=['POST'])
def milvus_search():
    data = request.get_json()
    query = data['query']
    print(f"Received JSON data: {data}")

    if not query:
        return jsonify({"error": "Query parameter not provided"}), 400

    results = search(query)
    return jsonify({"results": results})


@milvus_bp.route('/logs', methods=['POST'])
def chat_logs():
    try:
        chat_data = request.get_json()
        
        conversation_id= chat_data.get('conversation_id')

        messages = chat_data.get('messages')
        print(messages)
        conversation = Conversation(
            conversation_id=conversation_id,
            messages=messages,
            created_at=datetime.utcnow()
        )

        db.session.add(conversation)

        db.session.commit()

        return jsonify({"success": True, "message": "Chat data added to the database successfully."}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500



def generate_data():
    data = [
        {"id": 1, "status": "This test db is running"},
    ]

    for item in data:
        yield f"Data: {item}\n"
        time.sleep(1)

@milvus_bp.route('/streaming_data')
def streaming_data():
    return Response(generate_data(), content_type='text/plain', status=200)
