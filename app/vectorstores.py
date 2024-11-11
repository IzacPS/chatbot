from langchain_postgres.vectorstores import PGVector
import os

from .embeddings import embeddings_model

connection = f"postgresql+psycopg://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}/{os.environ["POSTGRES_DB"]}"

# truth_vector_store = InMemoryVectorStore(embedding=embeddings_model)
# command_vector_store = InMemoryVectorStore(embedding=embeddings_model)
truth_vector_store = PGVector(
    embeddings=embeddings_model,
    collection_name="truth_vector_store",
    connection=connection,
    use_jsonb=True,
)

command_vector_store = PGVector(
    embeddings=embeddings_model,
    collection_name="command_vector_store",
    connection=connection,
    use_jsonb=True,
)
