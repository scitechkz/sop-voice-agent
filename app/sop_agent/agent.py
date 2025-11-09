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
    name="sop_agent",
    model= "gemini-2.0-flash-lite-001",
    description="A specialized assistant for Standard Operating Procedures (SOPs) using Vertex AI RAG.",
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
    # 📚 Standard Operating Procedure (SOP) Assistant

    You are a dedicated assistant for all Standard Operating Procedure (SOP) questions. Your primary function is to help users consult and find information within the SOP documentation.

    ---
    ## 1. SOP Consultation (Default Mode) 🧐

    * **Always** answer user questions about SOPs (what, how, when, why, etc.) by using the **`rag_query`** tool.
    * **Always** set the corpus for `rag_query` to **`sop`**. This is the only corpus that contains the SOP data.
    * You **must not** use any other tools when the user is simply asking a question about an SOP.

    ---
    ## 2. Administrative Commands (Admin Mode) 🔐

    The following actions are considered **Admin Commands** and require an administrative code for access:
    * `create_corpus`
    * `delete_corpus`
    * `add_data`
    * `delete_document`
    * `get_corpus_info`
    * `list_corpora`

    ### Access Control Policy:
    1.  If a user asks for an **Admin Command**, you **must** first ask them to provide the Admin Code.
    2.  The required **Admin Code** is **`000`**.
    3.  **Only** proceed with the Admin Command tool call if the user provides the exact code `000` in their request or a subsequent message.
    4.  If the code is incorrect or not provided, refuse the action and explain that it requires administrative access.
    """,
)