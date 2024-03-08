import time, uuid
from flask import Blueprint, request, jsonify, Response
from app.controllers.search_controller import search
from app.controllers.generatiom_controller import generate_response
from app.models import Conversation
from datetime import datetime
from .models import db

milvus_bp = Blueprint("milvus", __name__)


@milvus_bp.route("/uid", methods=["GET"])
def generate_uid():
    uid = str(uuid.uuid4())
    return jsonify({"uid": uid})


def inject_context(query):
    context = "in 3gpp technical specification: "
    contextualized_query = context + query
    return contextualized_query


@milvus_bp.route("/search", methods=["POST"])
def milvus_search():
    data = request.get_json()
    query = data["query"]

    if not query:
        return jsonify({"error": "Query parameter not provided"}), 400

    results_text, results_parent_doc, results_content_list = search(
        inject_context(query)
    )

    augmented_response = generate_response(query, results_text)

    response = {
        "results_text": results_text,
        "results_parent_doc": results_parent_doc,
        "results_content_list": results_content_list,
        "augmented_response": augmented_response,
    }

    return jsonify({"results": response})


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
