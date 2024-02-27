from flask import Flask
from config import init_config
from pymilvus import connections

app = Flask(__name__)
init_config(app)


def init_milvus_connection():
    print("\n=== {:30} ===\n".format("Start connecting to Milvus"))
    connections.connect(
        "default",
        host=app.config['MILVUS_HOST'],
        port=app.config['MILVUS_PORT'],
        user=app.config['MILVUS_USER'],
        password=app.config['MILVUS_PASSWORD']
    )
    print("Connected to Milvus")




from app import routes, models
