import time
from flask import Blueprint, request, jsonify, Response
from app.controllers.search_controller import search
from app.controllers.generatiom_controller import generate_response
from app.models import Conversation
from datetime import datetime
from .models import db

milvus_bp = Blueprint("milvus", __name__)


def inject_context(query):
    context = "in 3gpp technical specification: "
    contextualized_query = context + query
    return contextualized_query 


@milvus_bp.route("/search", methods=["POST"])
def milvus_search():
    data = request.get_json()
    query = data["query"]
    print(f"Received JSON data: {data}")

    if not query:
        return jsonify({"error": "Query parameter not provided"}), 400

    results_text, results_parent_doc, results_content_list = search(inject_context(query))

    augmented_response = generate_response(query, results_text)
    print(augmented_response)

    response = {
        "results_text": results_text,
        "results_parent_doc": results_parent_doc,
        "results_content_list": results_content_list,
        "augmented_response": augmented_response
    }

    return jsonify({"results": response})


@milvus_bp.route("/logs", methods=["POST"])
def chat_logs():
    try:
        chat_data = request.get_json()

        conversation_id = chat_data.get("conversation_id")

        messages = chat_data.get("messages")
        print(messages)
        conversation = Conversation(
            conversation_id=conversation_id,
            messages=messages,
            created_at=datetime.utcnow(),
        )

        db.session.add(conversation)

        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Chat data added to the database successfully.",
                }
            ),
            200,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500