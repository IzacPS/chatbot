from langchain_huggingface import HuggingFaceEmbeddings

embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
# truth_vector_store = InMemoryVectorStore(embedding=embeddings_model)
# command_vector_store = InMemoryVectorStore(embedding=embeddings_model)
