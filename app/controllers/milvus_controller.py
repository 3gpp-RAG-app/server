from app import app, init_milvus_connection
from pymilvus import Collection
from openai import OpenAI

init_milvus_connection()

collection_name = "Group_Radio_Access_Network"
collection = Collection(collection_name)

print("collection loaded")


def embed(text):
    openai_client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
    response = openai_client.embeddings.create(
        input=text,
        model=app.config['OPENAI_ENGINE']
    )
    return response.data[0].embedding


def search(text):
    search_params={
        "metric_type": "L2"
    }

    results=collection.search(
        data=[embed(text)],  
        anns_field="embeding",  
        param=search_params,
        limit=5, 
        output_fields=['file_id', 'text_content', 'parent_doc']
    )

    ret=[]
    for hit in results[0]:
        row = [hit.id, hit.score, hit.entity.get('text_content'), hit.entity.get('parent_doc')]
        ret.append(row)

    ret.sort(key=lambda x: x[1])
    if ret:
        best_hit_id, best_hit_score, best_hit_text, best_hit_parent_doc = ret[0]
    return best_hit_text
