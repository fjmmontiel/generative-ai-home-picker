import os
import json
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain.chains import LLMChain
from chromadb.utils import embedding_functions
from ai_integration.langchain_functions import initialize_openai_client, create_prompt_template, generate_listings
from database_functions.chromaDB_functions import initialize_chromadb_client, add_listings_to_chromadb, get_total_documents, retrieve_listings, retrieve_all_listings
from dataModels import House

# Set Streamlit configuration
st.set_page_config(layout="wide")

# Load environment variables
load_dotenv()
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Streamlit App
st.title("Real Estate Listings Generator")

# Initialize clients
llm = initialize_openai_client()
chroma_client = initialize_chromadb_client()

# Create prompt template and LLM chain
prompt_template = create_prompt_template()
llm_chain = LLMChain(prompt=prompt_template, llm=llm)

# Create tabs for different functionalities
tabs = st.tabs(["Database Generation", "Home Seeker", "Database Management"])

# Database Generation Tab
with tabs[0]:
    
    st.header("Generate Listings for Database")
    number_of_listings = st.number_input("Number of listings to generate", min_value=1, max_value=100, value=2)
    generate_button = st.button("Generate Listings")
    if generate_button:
        try:
            # Generate listings
            houses_data = generate_listings(llm_chain, number_of_listings)
            houses = [House(**house_data) for house_data in houses_data]

            # Add house listings to the ChromaDB collection
            collection = add_listings_to_chromadb(houses, chroma_client, openai_api_key)
            st.success("Listings successfully added to ChromaDB collection.")

            # Display generated listings in a table
            listings_df = pd.DataFrame([house.dict() for house in houses])
            st.dataframe(listings_df, hide_index=True, use_container_width=True)

            # Retrieve and display total number of documents in the collection
            total_docs = get_total_documents(collection)
            st.write(f"Total number of documents in the collection: {total_docs}")

        except json.JSONDecodeError as e:
            st.error(f"Error parsing JSON: {e}")

# Home Seeker Tab
with tabs[1]:
    
    st.header("Retrieve Listings for Home Seekers")
    query_text = st.text_input("Query for retrieval", "house with 3 bedrooms in Los Angeles")
    retrieve_button = st.button("Retrieve Listings")
    if retrieve_button:
        try:
            embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=openai_api_key)
            collection_name = "real_estate_listings"
            if collection_name in [collection.name for collection in chroma_client.list_collections()]:
                collection = chroma_client.get_collection(name=collection_name, embedding_function=embedding_function)
                retrieved_listings = retrieve_listings(collection, query_text, n_results=5)
                st.success("Successfully retrieved the houses for your query!")
                # Extract and format the listings data
                formatted_listings = [json.loads(doc) for doc in retrieved_listings['documents'][0]]
                retrieved_listings_df = pd.DataFrame(formatted_listings)
                st.dataframe(retrieved_listings_df, hide_index=True, use_container_width=True)
            else:
                st.error("Collection not found. Please generate listings first.")

        except Exception as e:
            st.error(f"Error retrieving listings: {e}")

# Database Management Tab
with tabs[2]:
    st.header("Manage Database")   
    try:
        # Retrieve all listings when the tab is clicked
        collection = [collection for collection in chroma_client.list_collections()][0]
        all_listings = retrieve_all_listings(collection)["metadatas"]
        if all_listings:
            all_listings_df = pd.DataFrame([listing for listing in all_listings])
            st.dataframe(all_listings_df, hide_index=True, use_container_width=True)
            # Add a button to download all listings as a text file
            with open("Listings.txt", "w") as f:
                f.write(all_listings_df.to_string(index=False))
            st.download_button(label="Download Listings", data="Listings.txt", file_name="Listings.txt", mime="text/plain")
    except Exception as e:
        st.error(f"Error retrieving all listings: {e}")
   