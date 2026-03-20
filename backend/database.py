import os
from models import Pro

# Mock Data
MOCK_PROS = [
    Pro(id="1", name="Dave's Plumbing", profession="Plumber", location="San Francisco", description="Expert in pipe repair, leak detection, and water heaters.", rating=4.8, reviews=124),
    Pro(id="2", name="Quality Electric", profession="Electrician", location="San Francisco", description="Licensed electrician for wiring, panels, and lighting. 24/7 service.", rating=4.9, reviews=89),
    Pro(id="3", name="Sparkle Clean", profession="Cleaner", location="San Jose", description="Deep cleaning, move-in/move-out, and weekly cleaning services.", rating=4.7, reviews=56),
    Pro(id="4", name="SF Fix-It All", profession="Handyman", location="San Francisco", description="General repairs, furniture assembly, and drywall patching.", rating=4.5, reviews=210),
    Pro(id="5", name="Bay Area HVAC", profession="HVAC", location="San Jose", description="AC repair, furnace installation, and duct cleaning.", rating=4.9, reviews=150)
]

class MockFastVectorDB:
    """A Lightweight in-memory database to prevent OOM on Render Free Tier."""
    def __init__(self):
        self.is_initialized = False
        
    def _initialize_db(self):
        print("Initializing Lightweight Mock Database...")
        # Since we are bypassing PyTorch to save 500MB of RAM, we skip heavy embedding initialization.
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
        # Lightweight keyword match instead of vector embedding search to save RAM.
        query_words = query.lower().split()
        scored_pros = []
        
        for pro in MOCK_PROS:
            score = 0
            text_corpus = f"{pro.profession} {pro.location} {pro.description} {pro.name}".lower()
            for word in query_words:
                if len(word) > 3 and word in text_corpus:
                    score += 1
                if word in pro.profession.lower() or word in pro.location.lower():
                    score += 5 # high weight for profession/location
            scored_pros.append((score, pro))
            
        # Sort by score descending
        scored_pros.sort(key=lambda x: x[0], reverse=True)
        
        # Return top_k docs that have at least some relevance, otherwise return standard pros
        if scored_pros[0][0] > 0:
            return [p[1] for p in scored_pros[:top_k]]
        else:
            return MOCK_PROS[:top_k]

# Singleton DB instance
db = MockFastVectorDB()
