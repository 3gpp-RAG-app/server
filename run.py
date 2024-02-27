from flask import Flask
from flask_cors import CORS  
from app.routes import milvus_bp

app = Flask(__name__)
CORS(app)  

app.register_blueprint(milvus_bp, url_prefix='/milvus')

if __name__ == '__main__':
    app.run(debug=True)
