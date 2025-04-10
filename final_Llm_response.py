from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os

# Set your Groq API Key
os.environ["GROQ_API_KEY"] = "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"

# Load HuggingFace Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS vector DB
db = FAISS.load_local(
    "C:/Users/nagav/OneDrive/Desktop/lawStuff/FAISS_DB",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

# Query
query = "is giving dowry legal?"
top_k = 5
results = db.similarity_search(query, k=top_k)

# Create context from retrieved documents
context = "\n\n".join([doc.page_content for doc in results])

# Prompt template
prompt_template = """
You are a legal assistant AI. Use the following context from Indian law to answer the user's question and answer in 300 words.

Context:
{context}

Question: {question}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

# Load LLM from Groq (you can use "mixtral-8x7b-32768", "llama3-8b-8192", or "gemma-7b-it")
llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama3-8b-8192",
    temperature=0.3,
    max_tokens=1024
)

# Run RAG chain
rag_chain = LLMChain(prompt=prompt, llm=llm)
response = rag_chain.run({"context": context, "question": query})

# Print the final answer
print("\n💬 Final Answer:\n", response)
