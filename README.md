# 1 Get And Start Milvus

run the following commands

```bash
wget https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
bash standalone_embed.sh start
```

# 2 Create Milvus Collection And Insert Data

* [Create Collecction](data/scripts/create_collection.py)

* [Insert data into collection](data/scripts/insert_data.py)

# 3 Running Docker Compose

In the root directory of the app, you'll find a compose.yaml file. This file handle the creation of three images:

* Image ragend: Serving Endpoint (server-app) 

* Image mariadb: MySQL Database

* Image nmpimage:  Client side App [React-app](https://github.com/3gpp-RAG-app/react-app-v01.git)

For the server-app, you'll need to create a .env file to manage environment variables.
Below is the example of the expected .env file with placeholders for necessary variables:

 ```python
OPENAI_API_KEY=

HOST=127.0.0.1
MILVUS_PORT=19530
MILVUS_USER=user
MILVUS_PASSWORD=Milvus

MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DB="mysql"
MYSQL_ROOT_PASSWORD=123456

OPENAI_EMB_ENGINE=text-embedding-3-large
OPENAI_GEN_ENGINE=gpt-4-turbo-preview

```