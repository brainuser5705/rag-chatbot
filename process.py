import os
import dotenv

dotenv.load_dotenv()

from tkinter import filedialog

from rq import Queue
import time

from models.UnstructuredModel import Unstructured
from models.QdrantModel import Qdrant
from models.ChatbotModel import Chatbot
from langchain_openai import OpenAIEmbeddings
from models.UnstructuredModel import IngestionException
from models.QdrantModel import InsertionException

LM_STUDIOS_SERVER_URL = os.getenv("LM_STUDIOS_SERVER_URL")

embedding_model = OpenAIEmbeddings(
    base_url=LM_STUDIOS_SERVER_URL,
    api_key="lm-studios",
    check_embedding_ctx_length=False
)

unstructured = Unstructured()

qdrant = Qdrant(embedding_model=embedding_model)

chatbot = Chatbot()

def create_workspace(workspace_name):
    qdrant.create_collection_if_not_exists(workspace_name)

"""
Handles document uploads, organized them in a user-queried workspace and queues 
processing job for each upload.

:param: queue - Job queue to populate for each document upload
:param: message_label - Tkinter Label displaying status messages
"""
def upload_files(queue : Queue, workspace_name, message_label):

    file_paths = filedialog.askopenfilenames(title="Select a file to import")

    for file_path in file_paths:
        file_name = os.path.basename(file_path)

        result = queue.enqueue(process_file, workspace_name, file_path)
        time.sleep(2)
        if result is None:
            msg = f"File {file_name} failed to be processed..."
        else:
            msg = f"File {file_name} have been successfully processed!"
        message_label.config(text=msg)


"""
RAG pipeline process - document ingestion (Unstructured) and vector data storage
 (Qdrant)

:param: the workspace the file is stored in
"""
def process_file(workspace_name, file_path):
    
    try:
        chunks = unstructured.ingest_document(file_path=file_path)
        for chunk in chunks:
            qdrant.insert_point(workspace_name, chunk)

        return True

    except (IngestionException, InsertionException) as e:
        print(e)
        return None


"""
Searches the most relevant chunks in Qdrant and invokes the LLM for an answer.

:param: query - the user-entered query
"""
def ask_model(user_query, workspace_name):
    returned_chunks = qdrant.query_point(workspace_name, user_query)
    return chatbot.ask_question(str(returned_chunks), user_query)