import json
import os
from pymilvus import Collection, connections, utility
from config import HOST, MILVUS_PORT, MILVUS_PORT,MILVUS_USER, MILVUS_PASSWORD

connections.connect(
    "default", host=HOST, port=MILVUS_PORT, user=MILVUS_USER, password=MILVUS_PASSWORD
)
collection = Collection('NR_NG_RAN')
print('collection loaded')


def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def process_json_files(directory_path):
    counter = 0
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".json"):
            json_path = os.path.join(directory_path, filename)

            json_data = load_json(json_path)
            doc_title = json_data.get("title", "")
            text_titles = json_data.get("metadata_list", [])
            text = json_data.get("content_list", [])
            embeddings = json_data.get("embeddings", [])

            for i, emb in enumerate(embeddings):

                if len(emb) == 3072:
                    entity = [
                        [counter],
                        [doc_title],
                        [text_titles[i]],
                        [emb],
                        [f"{text_titles[i]} \n {text[i]}"],
                    ]
                    collection.insert(entity)
                    counter+=1
                    collection.flush()
                    print(
                        f"inserted {i} from {filename} \nembeddings list len is {len(embeddings)}"
                    )
                   
                else:
                    pass
                
            collection.release()


if __name__ == "__main__":
    process_json_files("data/jsons/383XX")
