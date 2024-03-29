from pymilvus import Collection
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
OPENAI_ENGINE = "text-embedding-3-large"
client.api_key = os.getenv("OPENAI_API_KEY")

search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = (3000,8)

collection = Collection("NR_NG_RAN")
collection.load()


def embed(text):
    response = client.embeddings.create(input=text, model=OPENAI_ENGINE)
    return response.data[0].embedding


def search(user_input):
    search_params = {"metric_type": "L2"}

    results = collection.search(
        data=[embed(user_input)],
        anns_field="embedings",
        param=search_params,
        limit=3,
        output_fields=["id", "original_text", "doc_title", "content_title"],
    )

    ret = []
    for hit in results[0]:
        row = [
            hit.score,
            hit.entity.get("original_text"),
            hit.entity.get("doc_title"),
            hit.entity.get("content_title"),
        ]
        ret.append(row)

    ret.sort(key=lambda x: x[1])

    if ret:
        return ret

    else:
        print("No results found.")
        return [None]
