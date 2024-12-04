
This script is a Streamlit-based web application for generating, managing, and retrieving real estate listings.
It leverages OpenAI's LLM capabilities via LangChain, ChromaDB for document storage and retrieval, and Streamlit for user interaction.

### Key Components
1. **Imports**: Necessary libraries and modules are imported, including `os`, `json`, `pandas`, `dotenv`, `streamlit`, and custom modules.
2. **Environment Variables**: `.env` file is loaded to access sensitive keys like OpenAI API credentials.
3. **Streamlit Configuration**: The app layout is set to "wide" for better presentation.
4. **Title**: The app's title is set to "Real Estate Listings Generator".
5. **Client Initialization**:
   - OpenAI client is initialized using `initialize_openai_client()`.
   - ChromaDB client is initialized using `initialize_chromadb_client()`.
6. **Prompt Template**: A prompt template for LLMChain is created using `create_prompt_template()`.
7. **Tabs**:
   - **Database Generation**:
     - Allows users to generate a specified number of real estate listings.
     - The generated listings are stored in ChromaDB and displayed in a table.
     - Total number of documents in the database is shown.
   - **Home Seeker**:
     - Enables querying the database to retrieve listings based on user input.
     - Results are displayed in a table after querying ChromaDB.
   - **Database Management**:
     - Lists all stored documents in the database.
     - Provides an option to download all listings as a text file.

### Features
1. **Database Creation**:
   - Users specify the number of listings.
   - Generated listings are stored in ChromaDB using the OpenAI API.
2. **Query and Retrieval**:
   - Users enter queries to fetch matching listings from the database.
   - Results are retrieved using embedding functions for semantic similarity.
3. **Database Management**:
   - Users can view all stored listings.
   - Provides an option to download the database as a text file.

### Error Handling
- JSON decoding errors during listing generation are caught and displayed.
- Errors during retrieval and database management are also handled gracefully.

### Dependencies
- `langchain` for LLM integration.
- `chromadb` for vector storage and retrieval.
- `streamlit` for creating the interactive web application.
- `dotenv` for managing environment variables.
- `pandas` for data manipulation and presentation.

The app is structured to provide a seamless user experience for managing real estate listings using cutting-edge AI and database tools.
