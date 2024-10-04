import yaml
from langchain_community.utilities import SQLDatabase
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

from src.settings import OPENAI_API_KEY, DEFAULT_MODEL, DB_HOSTNAME, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_PORT


class VannaSetup(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

vanna = VannaSetup(
    config={
        'api_key': OPENAI_API_KEY,
        'model': DEFAULT_MODEL,
    },
)
rds_uri = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
database = SQLDatabase.from_uri(rds_uri)

vanna.connect_to_postgres(
    host=DB_HOSTNAME,
    dbname=DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    port=int(DB_PORT),
)

def load_samples():
    sql_samples = None
    with open("src/moma_examples.yaml", "r") as stream:
        sql_samples = yaml.safe_load(stream)
    return sql_samples

def train_model():
    vanna.train(
        documentation="Base de datos con información artistas y obras de arte",
    )
    # Train with database schema
    database_schema = database.get_table_info()
    vanna.train(ddl=database_schema)

    # Train with SQL samples
    samples = load_samples()
    for sample in samples:
        vanna.train(
            question=sample['input'],
            sql=sample['sql_cmd'],
        )
    training_data = vanna.get_training_data()
    # print(training_data)