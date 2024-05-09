from pymilvus import Collection
from openai import OpenAI
from typing import Dict
import numpy as np
from config.settings import Config




client = OpenAI()
OPENAI_ENGINE = Config.OPENAI_EMB_ENGINE
client.api_key = Config.OPENAI_API_KEY

search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = (3000, 8)

collection = Collection("NR_NG_RAN")
collection.load()


def embed(text):
    response = client.embeddings.create(
        input=text, model=OPENAI_ENGINE
    )  # dimensions=1024
    return response.data[0].embedding


def search(user_input):
    search_params = {"metric_type": "L2"}

    results = collection.search(
        data=[embed(user_input)],
        anns_field="embedings",
        param=search_params,
        limit=6,
        output_fields=["id", "original_text", "doc_title", "content_title"],
    )

    ret = []
    for hit in results[0]:
        row = [
            hit.score,
            hit.entity.get("id"),
            hit.entity.get("original_text"),
            hit.entity.get("doc_title"),
            hit.entity.get("content_title"),
        ]
        ret.append(row)

    ret.sort(key=lambda x: x[0])

    return ret


def final_ranking(queries_list):
    rets = []
    id_scores = {}
    id_counts = {}

    for query in queries_list:

        for result in search(query):
            score, entity_id = result[0], result[1]
            print(result[0], result[3], result[4], result[1])
            if entity_id in id_scores:
                id_scores[entity_id][0] += score
                id_counts[entity_id] += 1
            else:

                id_scores[entity_id] = [score, result]
                id_counts[entity_id] = 1
                rets.append(result)

    for entity_id, score_data in id_scores.items():
        score_data[0] /= id_counts[entity_id]

    rets.sort(key=lambda x: x[0])
    rets = rets[:4]

    return rets
