# Basic LangChain example with prompt templates and document handling
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


def main():
    print("Hello World - LangChain Example")
    
    prompt_template = PromptTemplate(
        input_variables=["greeting"],
        template="Please respond to this greeting: {greeting}"
    )
    
    print("Created a simple prompt template")
    
    documents = [
        Document(page_content="Hello world! Welcome to LangChain."),
        Document(page_content="LangChain is a framework for developing applications powered by language models."),
        Document(page_content="This is a simple hello world example using LangChain.")
    ]
    
    print(f"Created {len(documents)} sample documents")
    
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)
        print("Successfully created vector store with embeddings")
        
        retriever = vectorstore.as_retriever()
        results = retriever.get_relevant_documents("hello world")
        
        print("\nRelevant documents:")
        for doc in results:
            print(f"- {doc.page_content}")
            
    except Exception as e:
        print(f"Note: Vector store creation requires OpenAI API key: {e}")
        print("Showing documents without embeddings:")
        for doc in documents:
            print(f"- {doc.page_content}")


if __name__ == "__main__":
    main()
