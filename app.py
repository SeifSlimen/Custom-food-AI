import streamlit as st
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Foodie AI", page_icon="🍲")

# Load vector store and embeddings once on app startup
@st.cache_resource(show_spinner=False)
def load_vectorstore():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    try:
        return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True), embeddings
    except Exception as e:
        st.error(f"❌ Failed to load vector store: {e}")
        return None, None

vectorstore, embeddings = load_vectorstore()
if vectorstore is None:
    st.stop()

retriever = vectorstore.as_retriever(search_kwargs={"k": 50})

# Initialize the LLM once
@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatOllama(model="llama3:instruct")

llm = get_llm()

# Prompt to ask each chunk (map step)
question_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful AI assistant that only answers food and recipe-related questions.

Use only the information in the context below. If the answer is not found in the context, reply:
"I don't know based on the data I have."

Do not explain your reasoning or include any internal thoughts.

Context:
{context}

Question: {question}

Answer:
"""
)

# Prompt to combine answers from chunks (reduce step)
combine_prompt = PromptTemplate(
    input_variables=["summaries", "question"],
    template="""
You are a helpful AI assistant combining information from multiple pieces of context to answer the question.

Use the following summaries to answer the question below.

Summaries:
{summaries}

Question: {question}

Answer:
"""
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="map_reduce",
    return_source_documents=True,
    chain_type_kwargs={
        "question_prompt": question_prompt,
        "combine_prompt": combine_prompt,
    }
)

st.markdown("""
    <h1 style='text-align: center; color: #d2691e;'>🍲 Foodie AI: Your Recipe & Cooking Assistant 🍲</h1>
    <p style='text-align: center; color: #6b4f1d;'>Ask about recipes, ingredients, or cooking steps!</p>
    <hr style='border-top: 2px solid #d2691e;'>
""", unsafe_allow_html=True)

user_input = st.text_input("What food or recipe question do you have?")

if user_input:
    with st.spinner("Looking for delicious answers..."):
        try:
            rag_result = qa_chain.invoke({"query": user_input})
            answer = rag_result['result']
            st.success(answer)

            source_docs = rag_result.get('source_documents', [])
            if source_docs:
                st.markdown("### 📚 Source Documents")
                for doc in source_docs:
                    source = doc.metadata.get('source', 'Your Recipe Dataset')
                    st.markdown(f"**Source:** {source}")
                    st.write(doc.page_content)
                    st.markdown("---")
        except Exception as e:
            st.error(f"❌ Error generating answer: {e}")
