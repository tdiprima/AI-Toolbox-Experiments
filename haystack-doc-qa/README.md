## Q\&A Bot for Tech Blog PDFs using Haystack

[Haystack](https://haystack.deepset.ai/) is an open-source NLP framework that makes it easy to build production-ready search systems and intelligent agents. In this example, you'll use Haystack to build a **Q\&A bot** that indexes a folder of technical blog PDFs and lets you ask natural language questions like:
**"What's the best practice for async in Python?"**
It'll return answers with **sourced excerpts** from your PDF documents—no need to manually dig through them.

### Assumptions

* You have a folder of PDFs (`./tech_blogs/`).
* You want to use a local BM25Retriever (no embeddings or vector DBs).
* You want to use a PromptNode (like OpenAI's GPT models) to generate coherent answers.
* You want answers to cite the specific PDF snippets they're based on.

## 1. Install Required Packages

```bash
pip install 'farm-haystack[all]' pypdf
```

## 2. Index PDFs

```python
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import PDFToTextConverter, PreProcessor
from haystack.nodes import BM25Retriever
from haystack.pipelines import Pipeline

import glob

# 1. Initialize an in-memory document store (no external DB needed)
document_store = InMemoryDocumentStore()

# 2. Set up PDF-to-text converter and text preprocessor
converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    split_by="word",              # Split docs based on word count
    split_length=200,             # Target chunk size
    split_overlap=20,             # 20-word overlap between chunks for context continuity
    split_respect_sentence_boundary=True  # Avoid breaking sentences
)

docs = []
for pdf_file in glob.glob("./tech_blogs/*.pdf"):
    # Convert the PDF to raw text (returns a dict with 'text' field)
    converted = converter.convert(file_path=pdf_file, meta={"name": pdf_file})
    
    # Split the text into smaller overlapping chunks for better retrieval
    processed = preprocessor.process(converted)
    
    docs.extend(processed)

# 3. Write processed document chunks into the document store
document_store.write_documents(docs)
```

## 3. Build Haystack Pipeline

```python
from haystack.nodes import PromptNode, PromptTemplate

# 1. BM25Retriever performs lexical keyword search across document chunks
retriever = BM25Retriever(document_store=document_store)

# 2. PromptNode wraps a language model (OpenAI, Cohere, etc.) for answer generation
prompt_node = PromptNode(
    model_name_or_path="gpt-4o",  # You can use any OpenAI model here
    api_key="your-openai-api-key",  # Replace with your real API key
    default_prompt_template=PromptTemplate(
        name="qa_with_sources",
        prompt_text=(
            "Given the following context excerpts from tech blogs, "
            "answer the question. Cite the relevant excerpt(s) in your answer.\n\n"
            "Context:\n{join(documents)}\n\nQuestion: {query}\n\nAnswer:"
        )
    ),
    max_length=512,
    model_kwargs={"temperature": 0.2}  # Low temp = more focused, deterministic answers
)

# 3. Build pipeline by chaining the retriever and the PromptNode
pipe = Pipeline()
pipe.add_node(component=retriever, name="Retriever", inputs=["Query"])
pipe.add_node(component=prompt_node, name="PromptNode", inputs=["Retriever"])
```

## 4. Query the Pipeline

```python
query = "What's the best practice for async in Python?"

# Run the pipeline with the query
result = pipe.run(query=query, params={"Retriever": {"top_k": 5}})

# Output the answer and show which documents/sources were used
print("Answer:", result["answers"][0].answer)

print("\nSources:")
for doc in result["answers"][0].meta["documents"]:
    print(f"- {doc.meta.get('name', 'Unknown')} (Excerpt: {doc.content[:200]}...)")
```

### How It Works

* Haystack retrieves **top\_k** relevant document chunks using BM25 (a keyword-matching algorithm).
* The PromptNode feeds those chunks to a language model (like GPT-4) to generate a concise answer.
* The model is prompted to **cite sources** from the input excerpts, so you know where the info came from.

## 5. Tips

* For better performance with large datasets, switch to `FAISSDocumentStore` or `ElasticsearchDocumentStore`.
* Tune `split_length` and `top_k` to match your dataset and answer quality goals.
* During PDF conversion, set `meta={"name": pdf_file}` so you can track which file each chunk came from (great for source attribution).
* You can cache or pre-process embeddings later if you switch to vector search.

### ✅ Summary

You've now built a smart Haystack Q\&A pipeline that:

* Indexes a folder of tech blog PDFs
* Uses BM25Retriever to find relevant chunks
* Passes them to a PromptNode that generates clear answers with citations

Perfect for building internal search tools, bots for tech teams, or even chat-based doc assistants.

<br>
