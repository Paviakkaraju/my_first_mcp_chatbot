import fitz
import nltk
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from docx import Document

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    result = "\n".join(full_text).strip()
    if not result:
        raise ValueError("No text extracted from the Word document.")
    return result


nltk.download('punkt')

def semantic_chunking(text, model_name='all-MiniLM-L6-v2', similarity_threshold=0.75):
    # Step 1: Sentence Segmentation
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        raise ValueError("No sentences found in the input text.")

    # Step 2: Embedding Generation
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences)

    # Ensure embeddings are 2D
    embeddings = np.array(embeddings)
    if embeddings.ndim != 2 or len(embeddings) < 2:
        return [' '.join(sentences)]

    # Step 3: Similarity Computation and Distance Matrix
    similarity_matrix = cosine_similarity(embeddings)
    distance_matrix = 1 - similarity_matrix

    # Step 4: Clustering
    clustering_model = AgglomerativeClustering(
        metric='precomputed',     # For sklearn <=1.2
        linkage='average',
        distance_threshold=1 - similarity_threshold,
        n_clusters=None
    )
    clustering_model.fit(distance_matrix)
    labels = clustering_model.labels_

    # Step 5: Combine sentences in the same cluster
    clustered_chunks = {}
    for sentence, label in zip(sentences, labels):
        clustered_chunks.setdefault(label, []).append(sentence)

    # Sort clusters by label and merge sentences into final chunks
    final_chunks = [' '.join(clustered_chunks[label]) for label in sorted(clustered_chunks)]

    return final_chunks

if __name__ == "__main__":
    docx_path = "New content for codework website.docx"
    text = extract_text_from_docx(docx_path)
    chunks = semantic_chunking(text)

    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---\n{chunk}")