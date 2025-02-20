"""currently named tools file, but could be renamed as connections"""
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
mdb_user = os.getenv("mdb_user")
mdb_password = os.getenv("mdb_password")
mongo_db_url = f"mongodb+srv://aapeebles:{mdb_password}@policycluster.nwfe5.mongodb.net/?retryWrites=true&w=majority&appName=policyCluster"


def get_postgres_engine():
    """rather than repeat the load dotenv a million time, create a function for it"""
    # Construct the SQLAlchemy connection string
    database_url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    # Create the SQLAlchemy engine
    engine = create_engine(database_url)
    return engine


def get_mongo_client():
    """singular function for connection to mongo"""
    # Create a new client and connect to the server
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

test = get_mongo_client()

mongo_uri
MongoClient()