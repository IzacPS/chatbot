from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
import os

embeddings_model = None 
if os.environ.get("OPENAI_API_KEY"):
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")#HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
elif os.environ.get("GROQ_API_KEY"):
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
