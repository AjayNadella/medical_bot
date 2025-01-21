import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from chromadb.config import Settings
import chromadb

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key="your_api_key",
            model_name="llama-3.1-70b-versatile"
        )

        self.client = chromadb.PersistentClient(path="./chroma_db_backup")
        self.collection = self.client.get_collection(name="PregnancyHealth")

        

    def answer_question(self, user_question):
        
        retrieved_docs = self.collection.query(query_texts=[user_question], n_results=5)
        if not retrieved_docs or "documents" not in retrieved_docs:
            return "No relevant information found in the knowledge base."
        
        documents = retrieved_docs["documents"]
        retrieved_docs_text = "\n".join(
            doc if isinstance(doc, str) else " ".join(doc) for doc in documents
    )

        prompt_qa = PromptTemplate.from_template(
            """
    You are a highly knowledgeable and reliable medical assistant specialized in women's health and pregnancy-related topics. 
    You provide accurate, concise, and empathetic answers to user queries based on the provided knowledge base and your own expertise.

    ### KNOWLEDGE BASE:
    The following information has been retrieved from the medical knowledge base:
    {document_context}

    ### QUESTION:
    {user_question}

    ### INSTRUCTION:
    - Use the information in the knowledge base to craft your response.
    - If the knowledge base does not contain sufficient information to fully answer the question, supplement your response with your own medical expertise.
    - Provide your answer in a clear and concise format, suitable for a layperson.

    ### ANSWER:
    """
            
        )

        # Chain the prompt with the LLaMA model
        chain_qa = prompt_qa | self.llm

        try:
            response = chain_qa.invoke(
                input={"document_context": retrieved_docs_text, "user_question": user_question}
            )
            answer = response.content.strip()
        except Exception as e:
            raise Exception(f"Failed to answer the question: {str(e)}")

        return answer

if __name__ == "__main__":
    print("your_api_key")
