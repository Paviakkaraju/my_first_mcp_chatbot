from flask import Flask, request, jsonify
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Init Qdrant + Embedding Model
qdrant_client = QdrantClient(host='localhost', port=6333)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
collection_name = "codework_refined_chunks"

@app.route('/mcp', methods=['POST'])
def mcp_handler():
    data = request.get_json()
    method = data.get('method')
    context = data.get('context', {})
    user_input = context.get('input', '')

    if method == 'retrieve':
        query_vector = embedding_model.encode(user_input).tolist()
        search_result = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=5
        )
        chunks = [hit.payload.get('text', '') for hit in search_result]
        return jsonify({'retrieved_chunks': chunks})
    return jsonify({'error': 'Unsupported method'}), 400

@app.route('/mcp', methods=['POST'])
def handle_mcp():
    data = request.get_json()
    # Do something with `data`
    return jsonify({"response": "Hello from MCP"})

if __name__ == '__main__':
    app.run(port=8000)
