
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("SUPABASE_KEY")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
mongo_uri = os.getenv("mdb_connection")


def get_postgres_engine():
    # Construct the SQLAlchemy connection string
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    return engine


def get_mongo_client():
    # Create a new client and connect to the server
    client = MongoClient(mongo_uri = os.getenv("mdb_connection")
    , server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)