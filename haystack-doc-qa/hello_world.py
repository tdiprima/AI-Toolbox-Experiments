# Shows document storage and retrieval using Haystack's in-memory document store
from haystack import Document, Pipeline
from haystack.components.writers import DocumentWriter
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore


def main():
    print("Hello World - Haystack Example")
    
    document_store = InMemoryDocumentStore()
    
    documents = [
        Document(content="Hello world! This is a simple Haystack example."),
        Document(content="Haystack is a powerful framework for building search applications."),
        Document(content="Welcome to the world of document search and retrieval!")
    ]
    
    writer = DocumentWriter(document_store=document_store)
    writer.run(documents=documents)
    
    print(f"Stored {len(documents)} documents in the document store")
    
    retriever = InMemoryBM25Retriever(document_store=document_store)
    results = retriever.run(query="hello world")
    
    print("\nRetrieved documents:")
    for doc in results["documents"]:
        print(f"- {doc.content}")


if __name__ == "__main__":
    main()
