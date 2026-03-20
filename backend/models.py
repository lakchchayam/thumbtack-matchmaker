from pydantic import BaseModel
from typing import List, Optional

class Pro(BaseModel):
    id: str
    name: str
    profession: str
    location: str
    description: str
    rating: float
    reviews: int

class UserRequest(BaseModel):
    query: str
    
class AgentResponse(BaseModel):
    response: str
    pros: List[Pro] = []
