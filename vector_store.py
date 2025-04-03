import os
import csv
import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


class VectorStore:
    """Handles vector embeddings for past ticket history and conversations."""

    def __init__(self, persist_directory="vector_store/chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="support_cases")
        self.embedder = OllamaEmbeddings(model="llama3.2")

    def add_document(self, doc_id, text):
        """Stores a document with its embedding."""
        embedding = self.embedder.embed_query(text)
        self.collection.add(
            ids=[doc_id], 
            embeddings=[embedding], 
            metadatas=[{"text": text}]
        )

    def query_similar(self, query_text, top_k=3):
        """Retrieves similar past cases based on vector similarity."""
        query_embedding = self.embedder.embed_query(query_text)
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )
        return results["metadatas"]

    def load_data(self, data_folder="data"):
        """Reads historical tickets and past conversations to populate vector store."""
        
        # Load from CSV file (Historical_ticket_data.csv)
        csv_file = os.path.join(data_folder, "Historical_ticket_data.csv")
        if os.path.exists(csv_file):
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    ticket_text = f"Issue: {row[' Issue Category']}, Sentiment: {row[' Sentiment']}, Resolution: {row[' Solution']}"
                    self.add_document(f"ticket_{i}", ticket_text)

        # Load from conversation transcripts
        conversation_folder = os.path.join(data_folder, "conversations")
        if os.path.exists(conversation_folder):
            for filename in os.listdir(conversation_folder):
                file_path = os.path.join(conversation_folder, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read().strip()
                    self.add_document(filename, text)

# Run only once to populate the vector store
if __name__ == "__main__":
    store = VectorStore()
    store.load_data()
    print("Vector store populated successfully!")
