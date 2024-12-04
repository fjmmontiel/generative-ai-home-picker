import os
import json
import re
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from chromadb.utils import embedding_functions
# Load environment variables from .env file
# load_dotenv("../.env")
load_dotenv()
model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
temperature = float(os.getenv("OPENAI_TEMPERATURE", 1.2))
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")
embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=openai_api_key)

# Function to initialize OpenAI client
def initialize_openai_client():
    return ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=2000, openai_api_key=openai_api_key, openai_api_base=openai_api_base)

# Function to create prompt template
def create_prompt_template():
    return PromptTemplate.from_template(
        """You are a real estate expert tasked with creating {number_of_listings} diverse and realistic real estate listings. Each listing should be in JSON format and include the following fields:
            - Title: A catchy and descriptive title.
            - Description: A brief overview highlighting key features.
            - Price: The property's market value.
            - Location: City and neighborhood.
            - Number of Rooms: Total rooms.
            - Number of Bathrooms: Total bathrooms.
            - Distance to City Center: Proximity to the nearest city center in kilometers.

            Follow the ReAct technique:
            1. Thought: Consider the need for diversity. Each listing should vary in property type (e.g., apartment, house, condo), price range, location (urban, suburban, rural), and unique features (e.g., swimming pools, gardens, proximity to schools).
            2. Action: Generate a listing with all specified details.
            3. Observation: Review the generated listing to ensure it meets the criteria.

            Repeat this Thought → Action → Observation cycle to generate all {number_of_listings} listings, ensuring each listing is unique, diverse, and realistic. Ensure the output is a JSON array of {number_of_listings} listings.
        """
    )

# Function to generate listings using LLM
def generate_listings(llm_chain, number_of_listings):
    output = llm_chain({"number_of_listings": number_of_listings})
    clean_output = re.sub(r'^```json\n|```$', '', output["text"]).strip()
    return json.loads(clean_output)