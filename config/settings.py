import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    HOST = os.getenv("HOST")
    MILVUS_PORT = os.getenv("MILVUS_PORT")
    MILVUS_USER =  os.getenv("MILVUS_USER")
    MILVUS_PASSWORD =  os.getenv("MILVUS_USER")

    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_EMB_ENGINE = os.getenv("OPENAI_EMB_ENGINE")
    OPENAI_GEN_ENGINE = os.getenv("OPENAI_GEN_ENGINE")



def load_config():
    return Config
