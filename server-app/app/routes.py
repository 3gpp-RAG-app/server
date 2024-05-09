import time, uuid
from flask import Blueprint, request, jsonify, Response
from app.controllers.search_controller import final_ranking
from app.controllers.generation_controller import generate_response
from app.controllers.expand_queries import expand_query
from app.models import Conversation
from datetime import datetime
from .models import db

milvus_bp = Blueprint("milvus", __name__)


@milvus_bp.route("/uid", methods=["GET"])
def generate_uid():
    uid = str(uuid.uuid4())
    return jsonify({"uid": uid})


@milvus_bp.route("/search", methods=["POST"])
def milvus_search():
    data = request.get_json()
    query = data["query"]

    if not query:
        return jsonify({"error": "Query parameter not provided"}), 400

    
    ret_list = final_ranking(expand_query(query))

    augmented_response = generate_response(query, ret_list)
    if "I could not find an answer." in augmented_response:
        return jsonify({"augmented_response": augmented_response})
    
    if ret_list:
        retrivals_list = []

        for ret in ret_list:
            ret_score, ret_id, ret_text, ret_parent_doc, ret_content_list = ret
            retrival = {
                "id" : ret_id,
                "score": ret_score,
                "text": ret_text,
                "parent_doc": ret_parent_doc,
                "content_list": ret_content_list,
            }
            retrivals_list.append(retrival)

    response = {
        "retrivals": retrivals_list,
        "augmented_response": augmented_response
    }

    return jsonify(response)


@milvus_bp.route("/logs", methods=["POST"])
def chat_logs():
    try:
        uid = request.form['uid']
        logs = request.form['logs']

        conversation = Conversation(
            conversation_id=uid,
            messages=logs,
            created_at=datetime.utcnow(),
        )

        db.session.add(conversation)

        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                }
            ),
            200,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500

