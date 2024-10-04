import os

from vanna.chromadb import ChromaDB_VectorStore
from vanna.openai import OpenAI_Chat

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DB_HOSTNAME = os.getenv('DB_HOSTNAME')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DEFAULT_MODEL = 'gpt-4o-mini'



class VannaSetup(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)