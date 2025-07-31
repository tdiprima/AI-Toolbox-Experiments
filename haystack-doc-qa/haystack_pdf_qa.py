from haystack import Document, Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.utils import Secret

import os
import glob

# Init Document Store
document_store = InMemoryDocumentStore()

# Convert PDFs to documents
converter = PyPDFToDocument()
splitter = DocumentSplitter(split_by="word", split_length=200, split_overlap=20)

docs = []
for pdf_file in glob.glob("./tech_blogs/*.pdf"):
    # Convert PDF to documents
    converted = converter.run(sources=[pdf_file])
    # Split documents
    split_docs = splitter.run(documents=converted["documents"])
    docs.extend(split_docs["documents"])

# Write documents to the DocumentStore
document_store.write_documents(docs)

# Components
retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = PromptBuilder(
    template="Given the following context excerpts from tech blogs, answer the question. Cite the relevant excerpt(s) in your answer.\n\nContext:\n{% for document in documents %}\n{{ document.content }}\n{% endfor %}\n\nQuestion: {{ query }}\n\nAnswer:",
    required_variables=["documents", "query"]
)
generator = OpenAIGenerator(
    model="gpt-4o",
    api_key=Secret.from_env_var("OPENAI_API_KEY"),
    generation_kwargs={"temperature": 0.2, "max_tokens": 512}
)

# Pipeline
pipe = Pipeline()
pipe.add_component("retriever", retriever)
pipe.add_component("prompt_builder", prompt_builder)
pipe.add_component("llm", generator)

pipe.connect("retriever", "prompt_builder.documents")
pipe.connect("prompt_builder", "llm")

query = "What's the best practice for async in Python?"
result = pipe.run(
    {
        "retriever": {"query": query, "top_k": 5},
        "prompt_builder": {"query": query}
    },
    include_outputs_from={"retriever", "prompt_builder", "llm"}
)

# Print answer and sources
print("Answer:", result["llm"]["replies"][0])
print("\nSources:")
for doc in result["retriever"]["documents"]:
    print(f"- {doc.meta.get('file_path', 'Unknown')} (Excerpt: {doc.content[:200]}...)")
