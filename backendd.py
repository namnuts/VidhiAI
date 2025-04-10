from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

import os

# --- Configuration ---
DATA_DIR = r"C:\Users\nagav\OneDrive\Desktop\lawStuff\legalPDF"
VECTOR_STORE_PATH = r"C:\Users\nagav\OneDrive\Desktop\lawStuff\FAISS_DB"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Set Groq API Key (make sure this is safe in production)
os.environ["GROQ_API_KEY"] = "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"

# --- FastAPI App ---
app = FastAPI(title="RAG Legal Chatbot API (Groq powered)")


from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or "*" for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Model ---
class QueryRequest(BaseModel):
    query: str

# --- Initialize Embeddings ---
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# --- Load Vector Store or Create It ---
if os.path.exists(VECTOR_STORE_PATH):
    print("🔁 Loading existing vector store...")
    vector_store = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)
else:
    print("📄 Loading PDFs and creating vector store...")
    documents = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_DIR, file))
            documents.extend(loader.load())
    vector_store = FAISS.from_documents(documents, embedding_model)
    vector_store.save_local(VECTOR_STORE_PATH)

# --- Prompt Template ---
prompt_template = """
You are a highly knowledgeable legal assistant AI. Use the following context from Indian legal documents to answer the user's question.
If the answer is not found in the context, give answer based on your own knoledgez.

Keep the response clear and around 300 words.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

# --- Initialize Groq LLM ---
llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama3-8b-8192",
    temperature=0.3,
    max_tokens=1024
)

# --- Create LLMChain for RAG ---
rag_chain = LLMChain(prompt=prompt, llm=llm)

# --- API Route ---
@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        docs = vector_store.similarity_search(request.query, k=5)
        context = "\n\n".join([doc.page_content for doc in docs])
        # response = rag_chain.run({"context": context, "question": request.query})
        response = rag_chain.invoke({"context": context, "question": request.query})

        return {
            "answer": response,
            "sources": [doc.metadata.get("source", "N/A") for doc in docs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "✅ Legal RAG Chatbot Backend is running!"}
