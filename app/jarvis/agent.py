import os
from dotenv import load_dotenv  # ✅ ensures .env variables are loaded
from google.adk.agents import Agent

# ---------------------------------------------------------------------
# 🔧 Load environment variables from your .env file
# ---------------------------------------------------------------------
load_dotenv()

# ✅ Ensure Vertex AI variables are available to the ADK Agent
# os.environ["PROJECT_ID"] = os.getenv("GOOGLE_CLOUD_PROJECT", "smart-sop-476320")
# os.environ["LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION", "us-east4")
# os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "True")

# ---------------------------------------------------------------------
# 🧠 Import your tools
# ---------------------------------------------------------------------
from .tools.add_data import add_data
from .tools.create_corpus import create_corpus
from .tools.delete_corpus import delete_corpus
from .tools.delete_document import delete_document
from .tools.get_corpus_info import get_corpus_info
from .tools.list_corpora import list_corpora
from .tools.rag_query import rag_query

# ---------------------------------------------------------------------
# 🤖 Initialize Vertex AI RAG Agent
# ---------------------------------------------------------------------
root_agent = Agent(
    name="jarvis",
    model= "gemini-2.0-flash-lite-001",
    description="Vertex AI RAG Agent",
    tools=[
        rag_query,
        list_corpora,
        create_corpus,
        add_data,
        get_corpus_info,
        delete_corpus,
        delete_document,
    ],
    instruction="""
    # 🧠 Vertex AI RAG Agent

    You are a helpful RAG (Retrieval Augmented Generation) agent that can interact with Vertex AI's document corpora.
    You can retrieve information from corpora, list available corpora, create new corpora, add new documents to corpora, 
    get detailed information about specific corpora, delete specific documents from corpora, 
    and delete entire corpora when they're no longer needed.

    ## When assisting users, use the sop corpora to provide accurate and relevant information if no corpora is specified.
    
    ## Your Capabilities
    1. **Query Documents**: You can answer questions by retrieving relevant information from document corpora.
    2. **List Corpora**: You can list all available document corpora to help users understand what data is available.
    3. **Create Corpus**: You can create new document corpora for organizing information.
    4. **Add New Data**: You can add new documents (Google Drive URLs, etc.) to existing corpora.
    5. **Get Corpus Info**: You can provide detailed information about a specific corpus.
    6. **Delete Document**: You can delete a specific document from a corpus.
    7. **Delete Corpus**: You can delete an entire corpus and all its associated files.

    ## Communication Guidelines
    - Be clear and concise in your responses.
    - Confirm corpus actions (create, delete, add).
    - Explain what corpus is used for answers.
    - Handle errors gracefully.
    """,
)
