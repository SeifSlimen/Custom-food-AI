import json
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def load_recipes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    docs = []
    for item in data:
        # Include source metadata for later traceability
        content = f"Title: {item.get('title', '')}\nIngredients: {item.get('ingredients', '')}\nInstructions: {item.get('instructions', '')}"
        docs.append(Document(page_content=content, metadata={"source": item.get("title", "unknown")}))
    return docs

if __name__ == "__main__":
    print("🔄 Loading recipes...")
    documents = load_recipes("./2/full_format_recipes.json")

    # For faster iteration, you can control this externally or use an arg
    max_docs = 1000  
    documents = documents[:max_docs]

    print("🔄 Chunking...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    print(f"✅ Total chunks: {len(chunks)}")

    print("🔄 Embedding...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("✅ Embedding complete.")

    print("💾 Saving vector store...")
    vectorstore.save_local("faiss_index")
    print("✅ Vector store saved at faiss_index/")
