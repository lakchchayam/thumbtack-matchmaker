import os
import chromadb
from models import Pro
from langchain_huggingface import HuggingFaceEmbeddings

# Mock Data
MOCK_PROS = [
    Pro(id="1", name="Dave's Plumbing", profession="Plumber", location="San Francisco", description="Expert in pipe repair, leak detection, and water heaters.", rating=4.8, reviews=124),
    Pro(id="2", name="Quality Electric", profession="Electrician", location="San Francisco", description="Licensed electrician for wiring, panels, and lighting. 24/7 service.", rating=4.9, reviews=89),
    Pro(id="3", name="Sparkle Clean", profession="Cleaner", location="San Jose", description="Deep cleaning, move-in/move-out, and weekly cleaning services.", rating=4.7, reviews=56),
    Pro(id="4", name="SF Fix-It All", profession="Handyman", location="San Francisco", description="General repairs, furniture assembly, and drywall patching.", rating=4.5, reviews=210),
    Pro(id="5", name="Bay Area HVAC", profession="HVAC", location="San Jose", description="AC repair, furnace installation, and duct cleaning.", rating=4.9, reviews=150)
]

class MockPostgresVectorDB:
    """Mocking Postgres + pgvector using ChromaDB for local prototyping."""
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name="thumbtack_pros")
        self.embeddings_model = None
        self.is_initialized = False
        
    def _initialize_db(self):
        if self.is_initialized:
            return
        print("Initializing Mock Vector Database...")
        try:
            self.embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        except Exception as e:
            print(f"Failed to load HuggingFace embeddings: {e}")
            return
        texts = [f"{pro.profession} in {pro.location}. {pro.description}" for pro in MOCK_PROS]
        embeddings = self.embeddings_model.embed_documents(texts)
        ids = [pro.id for pro in MOCK_PROS]
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=ids
        )
        self.is_initialized = True
        print(f"Added {len(MOCK_PROS)} pros to the database.")

    def get_all_pros(self):
        return MOCK_PROS

    def get_pro_by_id(self, pro_id: str) -> Pro:
        for pro in MOCK_PROS:
            if pro.id == pro_id:
                return pro
        return None

    def search_pros(self, query: str, top_k: int = 3) -> list[Pro]:
        if not self.is_initialized:
            self._initialize_db()
            
        if not self.is_initialized:
            # Fallback text search if no API key
            return MOCK_PROS[:top_k]
            
        query_embedding = self.embeddings_model.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        matched_pros = []
        if results and results.get('ids') and len(results['ids']) > 0:
            for doc_id in results['ids'][0]:
                pro = self.get_pro_by_id(doc_id)
                if pro:
                    matched_pros.append(pro)
        return matched_pros

# Singleton DB instance
db = MockPostgresVectorDB()
