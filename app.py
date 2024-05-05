from flask import Flask, render_template, request, jsonify
from sec_edgar_downloader import Downloader
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.palm import PaLM

app = Flask(__name__)

# Configure the LLAMA settings
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    device="cpu"
)
Settings.llm = PaLM(api_key="your_api_key_here")

# Load documents and create the index for LLAMA
documents_llama = SimpleDirectoryReader(r"C:/Users/DELL/Desktop/sec10k-RAG_Pipeline-master/data").load_data()
index_llama = VectorStoreIndex.from_documents(documents_llama)
query_engine_llama = index_llama.as_query_engine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    ticker = request.form['ticker']
    limit = request.form.get('limit')

    # Check if limit is not empty and convert to int
    if limit and limit.strip():  # Check if limit is not empty or whitespace
        limit = int(limit)
    else:
        limit = None  # Set limit to None if it's empty

    dl = Downloader("MyCompanyName", "my.email@domain.com")
    dl.get(form="10-K", ticker_or_cik=ticker, limit=limit, download_details=True)
    
    return jsonify({"success": True})

@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query']
    response = query_engine_llama.query(user_query)
    response_text = response.response
    
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
