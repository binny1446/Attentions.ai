from flask import Flask, request, jsonify
import arxiv
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel, pipeline
import torch
import fitz  # PyMuPDF for PDF extraction

# Initialize Flask app
app = Flask(__name__)

# Load Hugging Face pipeline for Q&A and summarization
qa_pipeline = pipeline("question-answering")
summarization_pipeline = pipeline("summarization")

# Initialize FAISS index (L2 distance, dimension 768 for embeddings)
faiss_index = faiss.IndexFlatL2(768)  # Assuming embedding size of 768

# Store metadata in a list (or you can use a database)
metadata = []

# Load the transformer model and tokenizer for generating embeddings
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to generate embeddings from text
def generate_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).cpu().numpy()
    return embeddings

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_url):
    doc = fitz.open(pdf_url)
    full_text = ""
    
    # Extract text from each page
    for page in doc:
        full_text += page.get_text()
    
    return full_text

# Function to add paper metadata and vector to FAISS
def add_paper_to_vector_db(paper_metadata, pdf_url):
    # Extract the full text from the PDF
    paper_text = extract_text_from_pdf(pdf_url)
    
    # Vectorize the full text of the paper
    embedding = generate_embedding(paper_text)
    
    # Convert embedding to float32 for FAISS
    embedding = np.array(embedding, dtype=np.float32)
    
    # Add the vector to FAISS index
    faiss_index.add(embedding)
    
    # Store metadata separately
    paper_metadata['full_text'] = paper_text  # Storing the full text along with other metadata
    metadata.append(paper_metadata)

# 1. Search Agent: Search for papers on arXiv
def search_papers(query, max_results=5):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = []
    for result in search.results():
        paper_metadata = {
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'summary': result.summary,
            'url': result.entry_id,
            'pdf_url': result.pdf_url  # Storing the URL to the PDF
        }
        
        # Add paper to FAISS vector database
        add_paper_to_vector_db(paper_metadata, paper_metadata['pdf_url'])

        results.append({
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'summary': result.summary,
            'url': result.entry_id
        })
    
    return results

# 2. Q&A Agent: Answer questions based on paper content
def answer_question(paper_text, question):
    return qa_pipeline(question=question, context=paper_text)

# 3. Future Work Agent: Generate future work suggestions based on papers
def generate_future_work(papers):
    summary = ""
    for paper in papers:
        summary += summarization_pipeline(paper['abstract'])[0]['summary_text']
    return f"Future research opportunities: {summary}"

# 4. Similarity Search: Find similar papers using FAISS
def search_similar_papers(query):
    query_embedding = generate_embedding(query)
    
    # Search for the most similar vectors
    _, indices = faiss_index.search(query_embedding, k=5)  # k is the number of similar papers
    
    similar_papers = []
    for idx in indices[0]:
        if idx != -1:
            similar_papers.append(metadata[idx])
    
    return similar_papers

# Route for searching papers (Search Agent)
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = search_papers(query)
    return jsonify(results)

# Route for answering questions about a paper (Q&A Agent)
@app.route('/qa', methods=['POST'])
def qa():
    data = request.get_json()
    paper_text = data['paper_text']
    question = data['question']
    answer = answer_question(paper_text, question)
    return jsonify(answer)

# Route for generating future work suggestions (Future Work Agent)
@app.route('/future_work', methods=['POST'])
def future_work():
    papers = request.get_json()['papers']
    future_work = generate_future_work(papers)
    return jsonify({"future_work": future_work})

# Route for querying similar papers based on vector similarity (Search Similar Papers)
@app.route('/similar_papers', methods=['GET'])
def similar_papers():
    query = request.args.get('query')
    similar_papers = search_similar_papers(query)
    return jsonify(similar_papers)

if __name__ == '__main__':
    app.run(debug=False)
