from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the FAISS DB with deserialization warning bypass (SAFE if your file is self-generated)
db = FAISS.load_local(
    "C:/Users/nagav/OneDrive/Desktop/lawStuff/FAISS_DB",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True  # ⚠️ Only use this if you trust the file source
)

# Query
query = "is giving dowry legal?"
top_k = 5

# Retrieve similar chunks
results = db.similarity_search(query, k=top_k)

# Print results
for i, doc in enumerate(results, 1):
    print(f"\n--- Result {i} ---\n{doc.page_content}")



# from langchain.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings

# # Load embeddings and FAISS index
# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# embedding_model = HuggingFaceEmbeddings(model_name=model_name)
# db = FAISS.load_local("C:/Users/nagav/OneDrive/Desktop/lawStuff/FAISS_DB", embedding_model)

# # Define your query and retrieval count
# query = "What are the powers of the Central Authority?"
# top_k = 5

# # Search
# results = db.similarity_search(query, k=top_k)

# # Display results
# print(f"\nTop {top_k} Results for: '{query}'")
# for i, doc in enumerate(results, start=1):
#     print(f"\n--- Result {i} ---")
#     print("Content:", doc.page_content)
#     if doc.metadata:
#         print("Metadata:", doc.metadata)
