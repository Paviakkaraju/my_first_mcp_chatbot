from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid
import json

# Step 1: Load extracted text from JSON
with open('chunks.json', 'r', encoding='utf-8') as f:
    extracted = json.load(f)

# Step 2: Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Open-source and fast
embedding_size = 384  # Dimension of MiniLM model

# Step 3: Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Step 4: Define collection name
collection_name = "codework_refined_chunks"

# Step 5: Create collection only if it doesn't exist
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE)
    )

# Step 6: Embed and prepare points
points = []

for entry in extracted:
    # Extract the title and text from each dictionary
    for title, text in entry.items():
        if not text.strip():  # Skip empty text values
            continue

        vector = model.encode(text)  # Generate the embedding vector for the text
        payload = {
            "title": title,
            "text": text
        }
        point_id = str(uuid.uuid4())  # Generate a unique ID for each point

        # Create PointStruct object for Qdrant
        points.append(
            PointStruct(
                id=point_id,
                vector=vector.tolist(),
                payload=payload
            )
        )

# Step 7: Upsert into Qdrant
client.upsert(collection_name=collection_name, points=points)

# Step 8: Confirm the upsert and print number of points
print(f"{len(points)} text blocks embedded and stored in Qdrant collection '{collection_name}'.")

# Optional: print current collections
print("Current collections:", client.get_collections())
