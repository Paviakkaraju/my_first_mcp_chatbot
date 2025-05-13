from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams, Filter

model = SentenceTransformer('all-MiniLM-L6-v2')
# Sample query text
query_text = "codework AI solutions"

# Step 1: Generate the query embedding
query_embedding = model.encode([query_text])[0]
client = QdrantClient(host="localhost", port=6333)

# Step 2: Perform a search in Qdrant
search_result = client.search(
    collection_name="codework_refined_chunks",
    query_vector=query_embedding.tolist(),
    limit=2,
    with_payload=True,
    search_params=SearchParams(hnsw_ef=128)
)
# Step 3: Display the search results
for result in search_result:
    print(f"ID: {result.id}, Text: {result.payload['text']}, Score: {result.score}")