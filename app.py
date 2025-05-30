import os 
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions

# Load the environment variables from .env 
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

## Some emebedding functions 
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key, 
    model_name="text-embedding-3-small"
)

# Initialize the chroma client with persistence 
chroma_client = chromadb.PersistentClient(
    path="chroma_persistent_storage"
)
collection_name = "document_qa_collection"
collection =chroma_client.get_or_create_collection(
    name=collection_name, 
    embedding_function=openai_ef
)

## Create openai client 
client = OpenAI(api_key=openai_key)

resp = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role":"system",
            "content":"You are a helpful assistant."
        },
        {
            "role":"user", 
            "content":"What is the life expectancy in the United States?"
        }
    ]
)

print(resp.choices[0].message.content)