#  Server-side 3GPP  RAG App 
 This application is written in Python and provides three API endpoints for managing User IDs, searching the vector database, and posting logs to the database.

 The purpose of this project is to enable users to perform similarity search of 3GPP (3rd Generation Partnership Project) documentation in a chat-like environment.

## Project Design
![Picture 1](/static/images/Slide3.jpg)

The flow is as follows: the server expects a user query in the request header.

The received query is then embedded and used to search the vector database.

The three best hits will be retrieved and given to the generate function, along with the original query, to generate an answer.

Once that is done, both the generated response to the user query from the retrieved source and the retrieved source itself are returned back to the user as an answer and its reference.

## Server Design
![Picture 2](/static/images/Slide4.jpg)

On the server level, the user query is first passed to a context injection function.

A short question that lacks clear context might be embedded in a representation that deviates further from its original intent.

The context injection function will tie the query to the topic of 3GPP specifications.

The contextualized query is then passed to the embedding function to produce its embedding, which is used by the search function to retrieve the best three matching rows of data.

These are delivered back to the user as sources and used as a reference by the generative model to generate an answer to the user.

Pairs of user questions and server responses along with user rating are collected per session and saved back to the server to be used later in further developing the app.

## Endpoints
Our project currently has 3 endpoints:

1. User ID Management
Endpoint: /uid
Description: Manages User IDs within the system.
Methods:
GET: Retrieves information about a specific User ID.
POST: Creates a new User ID.

2. Vector Database Search
Endpoint: /search
Description: Conducts similarity search in the vector database.
Methods:
POST: Performs a search based on user query and retrieves the best hits.

3. Logging
Endpoint: /logs
Description: Posts logs to the relational database.
Methods:
POST: Records logs in the database.

## Source Data And Query Embedings

We have chosen to work with floating-point embeddings.

We are utilizing the OpenAI embedding engine: **text-embedding-3-large to generate our embeddings.**

The default dimensions for the representations are **3072 dimensions.**

The query embedding shares the same dimensions as the embeddings stored in the database, i.e., **3072 dimensions.**

Note: We are currently working on integrating a specialized embedding model

## Data Storage
We are using [Milvus](https://milvus.io/), an open source storage solution to store, index, and manage vectors  and related metadata.

Milvus database is designed to handle vectors converted from unstructured data and queries over input vectors.

It has a built in search engine which makes it able to analyze the correlation between two vectors by calculating their similarity distance.

For floating points embeddings, Milvus metrics options are:

- Euclidean distance (L2) :It measures the length of a segment that connects 2 points.
- Inner product (IP) : It uses magnitude to filter results based on the importance or complexity of the sentences,  and angle to ensure that sentences are semantically related to the query.
- Cosine similarity (COSINE) :It uses the cosine of the angle between two sets of vectors to measure how similar they are

### Storage Concept
A Milvus collection is similar to a table in traditional databases and is used to store and manage data.

There is limitation how much data can be handled at the time (insert, loading, search …), so milvus by default uses MySQL/SQLite for metadata management. 

```python
fields = [
   FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
   FieldSchema(
       name="doc_title",
       dtype=DataType.VARCHAR,
       max_length=300,
       default_value="Unknown",
   ),
   FieldSchema(
       name="content_title",
       dtype=DataType.VARCHAR,
       max_length=600,
       default_value="Unknown",
   ),
   FieldSchema(name="embedings", dtype=DataType.FLOAT_VECTOR, dim=3072),
   FieldSchema(
       name="original_text",
       dtype=DataType.VARCHAR,
       max_length=65000,
       default_value="Unknown",
   ),
]
```
In Milvus data is handled as partitions of 512 MB.

Segment in partition is one row of data insert.

Mysql is created and updated within the milvus implementation. typically we don't have to care about it.

But in our case we are extending this implementation to utilise the relational setup in improving our storage strategy.

Refer to [Milvus guide](https://milvus.io/docs/v1.1.0/storage_concept.md)  for a comprehensive overview of Milvus storage concepts.

## Similarity Search

Our search function takes user’s query as parameter, it calls the embed function that is using OpenAI embedding engine: **text-embedding-3-large** to generate query embeddings.

then uses **the euclidean distance similarity metric** as its search parameter.

It retrieves best 3 hits along with their related metadata.

![Picture 3](/static/images/euclidean_metric.png)

where a = (a0, a1,..., an-1) and b = (b0, b0,..., bn-1) are two points in n-dimensional Euclidean space

Our points are floats, considering it being continuous data.

Euclidean distance is beneficial in our case, as it can measure the straight-line distance between float points in a continuous space.

The L2 metric measures the length of a segment that connects 2 points.

The smaller the distance value, the closer it is to the search query.

When we use Euclidean distance to identify the best match, we are locating the next closest point in the continuous vector representation. 

Note: Our choice of Euclidean distance (L2), is initial and we have to experiment more with other metrics and compare the results. based on  [Milvus Metrics guide](https://milvus.io/docs/metric.md#floating) metric L2 is beneficial when dealing with continuous data. 

## Response Generation
```python
def generate_response(query, ret_list):
  
   references = "\n".join([f"Reference Text: {ret[1]}, Reference Doc Title: {ret[2]}" for ret in ret_list])

   completion = client.chat.completions.create(
       model="gpt-4-turbo-preview",
       messages=[
           {
               "role": "system",
               "content": f'You are a 3GPP specialized assistant that answers to the user only based on the provided reference.'
                          f'If the answer can not be found in the given reference. respond "I could not find an answer."'
                          f'Here is the reference between brackets:[{references}].',
           },
           {"role": "user", "content": query},
       ],
       temperature=0.2,
       max_tokens=3000,
   )
   response_message = completion.choices[0].message
   return response_message.content
```
The system prompt is stricly instructing the generative model to answer users questions only from the providing answers unless it is found in the retreived "refrences".

That cause the model to refrain from generating answers if the information is not found in the retrieved source.

While this adds a layer of safety, source checking remains critical to ensure answers are derived from the correct documents.

##  Usage
Ensure you have Python installed on your system.
Install the required dependencies using pip install -r requirements.txt.
Set up your configuration in config/settings.py.
Activate the virtual environment (venv) using source venv/bin/activate.
Run the application using python run.py.
Access the API endpoints using appropriate HTTP methods and URIs as described above.
Additional Information
This project connects to two databases: Milvus (vector database) and MySQL (relational database).
It utilizes similarity search to retrieve the best hits from the vector database.
The retrieved hits are passed to a generative model to generate answers to user queries.
Finally, the application provides users with answers to their questions along with the source information returned in the server response from the search call.
For more detailed information, refer to the codebase and documentation within the project.

Contributing
Contributions are welcome! Please refer to the contribution guidelines in the CONTRIBUTING.md file for more details.