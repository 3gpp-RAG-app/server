from pymilvus import utility, FieldSchema, CollectionSchema, DataType, Collection, connections

def create_collection():
    #utility.drop_collection("Group_Radio_Access_Network")
    #print("deleted, and new being created")

    fields = [
        FieldSchema(name="file_id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="parent_doc", dtype=DataType.VARCHAR, max_length=200, default_value="Unknown"),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=3072),
        FieldSchema(name="text_content", dtype=DataType.VARCHAR, max_length=25000, default_value="Unknown")
    ]

    schema = CollectionSchema(
        fields=fields,
        description="Test file search",
        enable_dynamic_field=True
    )

    collection_name = "Group_Radio_Access_Network"

    if collection_name in connections.list_collections():
        print("Collection already exists. Reusing it.")
        collection = Collection(name=collection_name)
    else:
        collection = Collection(
            name=collection_name,
            schema=schema,
            using='default',
            shards_num=2
        )

        index_params = {
            'index_type': 'IVF_FLAT',
            'metric_type': 'L2',
            'params': {'nlist': 1024}
        }

        collection.create_index(field_name="embedding", index_params=index_params)

    return collection


