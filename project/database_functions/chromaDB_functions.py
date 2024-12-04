import uuid
import chromadb
from chromadb.utils import embedding_functions

# Function to initialize ChromaDB client
def initialize_chromadb_client():
    return chromadb.PersistentClient(path="./chromaDocs")

# Function to add listings to ChromaDB
def add_listings_to_chromadb(houses, chroma_client, openai_api_key):
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=openai_api_key)
    collection_name = "real_estate_listings"
    if collection_name in [collection.name for collection in chroma_client.list_collections()]:
        collection = chroma_client.get_collection(name=collection_name, embedding_function=embedding_function)
    else:
        collection = chroma_client.create_collection(name=collection_name, embedding_function=embedding_function)
    
    for house in houses:
        unique_id = str(uuid.uuid4())
        metadata = house.dict()
        metadata.update({"id": unique_id})  # Add unique ID to metadata
        collection.add(
            documents=[house.json()],
            metadatas=[metadata],
            ids=[unique_id]
        )
    return collection

# Function to retrieve listings from ChromaDB with optional filters
def retrieve_listings(collection, query_text, n_results=5, filters=None):
    # Adjust filters to use proper operator format
    formatted_filters = []
    if filters:
        if len(filters) > 1:
            for key, value in filters.items():
                formatted_filters.append({key: {"$eq": value}})
            where_clause = {"$and": formatted_filters}
        else:
            key, value = next(iter(filters.items()))
            where_clause = {key: {"$eq": value}}
    else:
        where_clause = None
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where_clause  # Optional filters based on metadata
    )
    return results

# Function to get total number of documents in a collection
def get_total_documents(collection):
    count = collection.count()
    return count

# Function to retrieve all listings from a collection
def retrieve_all_listings(collection):
    return collection.get()