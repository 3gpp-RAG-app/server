from pymilvus import Collection
from openai import OpenAI
import os
from typing import Dict

import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer


"""
os.environ['HF_HOME'] = "/opt/games/hugging_project/cache/"


# For retrieval you need to pass this prompt. Please find our more in our blog post.
def transform_query(query: str) -> str:

    return f'Represent this sentence for searching relevant passages: {query}'

# The model works really well with cls pooling (default) but also with mean poolin.
def pooling(outputs: torch.Tensor, inputs: Dict,  strategy: str = 'cls') -> np.ndarray:
    if strategy == 'cls':
        outputs = outputs[:, 0]
    elif strategy == 'mean':
        outputs = torch.sum(
            outputs * inputs["attention_mask"][:, :, None], dim=1) / torch.sum(inputs["attention_mask"])
    else:
        raise NotImplementedError
    return outputs.detach().cpu().numpy()

# 1. load model
model_id = 'mixedbread-ai/mxbai-embed-large-v1'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id).cuda()



def embed(input_text):
    docs = [
    transform_query(input_text)
    ]

    inputs = tokenizer(docs, padding=True, return_tensors='pt')
    for k, v in inputs.items():
        inputs[k] = v.cuda()
    outputs = model(**inputs).last_hidden_state
    embeddings = pooling(outputs, inputs, 'cls')
    return(embeddings[0])"""


from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
OPENAI_ENGINE = "text-embedding-3-large"
client.api_key = os.getenv("OPENAI_API_KEY")

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
