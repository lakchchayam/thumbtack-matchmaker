import os
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from models import Pro
from database import db

class AgentState(TypedDict):
    query: str
    intent: str
    is_safe: bool
    pros_found: List[Pro]
    final_response: str

# LLM setup (Expects GROQ_API_KEY)
def get_llm():
    if not os.environ.get("GROQ_API_KEY"):
        return None
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# 1. Safety Node
class SafetyCheck(BaseModel):
    is_safe: bool = Field(description="Whether the user request is safe, legal, and adheres to Thumbtack policies.")

def safety_node(state: AgentState):
    llm = get_llm()
    if not llm:
        return {"is_safe": True} # Fallback if no API key
        
    query = state.get("query", "")
    prompt = f"Analyze the following user query for safety, fraud, or policy violations. Just answer if it's safe. Query: '{query}'"
    structured_llm = llm.with_structured_output(SafetyCheck)
    try:
        result = structured_llm.invoke([HumanMessage(content=prompt)])
        return {"is_safe": result.is_safe}
    except Exception as e:
        print(f"Safety check error: {e}")
        return {"is_safe": True}

# 2. Intent Extraction
class IntentExtraction(BaseModel):
    intent: str = Field(description="The primary intent. Options: 'find_pro', 'general_greeting', 'unsafe'")
    extracted_search_terms: str = Field(description="If find_pro, the core search terms (e.g., 'plumber near me')")

def intent_node(state: AgentState):
    if not state.get("is_safe", True):
        return {"intent": "unsafe"}
        
    llm = get_llm()
    if not llm:
        return {"intent": "find_pro", "query": state.get("query", "")}
        
    query = state.get("query", "")
    prompt = f"Extract the intent and search terms from the query: '{query}'"
    structured_llm = llm.with_structured_output(IntentExtraction)
    try:
        result = structured_llm.invoke([HumanMessage(content=prompt)])
        return {"intent": result.intent, "query": result.extracted_search_terms}
    except Exception as e:
        print(f"Intent extraction error: {e}")
        return {"intent": "find_pro"} # Fallback

# 3. Matchmaker Retrieval
def matchmaker_node(state: AgentState):
    if state.get("intent") != "find_pro":
        return {"pros_found": []}
    
    query = state.get("query", "")
    pros = db.search_pros(query, top_k=2)
    return {"pros_found": pros}

# 4. Response Generator
def response_node(state: AgentState):
    intent = state.get("intent")
    
    if intent == "unsafe":
        return {"final_response": "I cannot help with that request as it violates our safety policies."}
    
    if intent == "general_greeting":
        return {"final_response": "Hello! I am the Thumbtack Matchmaker AI. Are you looking to hire a professional today?"}
        
    pros_found = state.get("pros_found", [])
    if not pros_found:
        return {"final_response": "I couldn't find any professionals matching your request right now. Try adjusting your search."}
        
    pro_names = ", ".join([p.name for p in pros_found])
    return {"final_response": f"I found some great professionals for you! I recommend checking out: {pro_names}."}

# Build Graph
builder = StateGraph(AgentState)
builder.add_node("safety", safety_node)
builder.add_node("intent", intent_node)
builder.add_node("matchmaker", matchmaker_node)
builder.add_node("response", response_node)

builder.add_edge(START, "safety")
builder.add_edge("safety", "intent")
builder.add_edge("intent", "matchmaker")
builder.add_edge("matchmaker", "response")
builder.add_edge("response", END)

workflow = builder.compile()

def run_agent(query: str):
    initial_state = {"query": query}
    try:
        result = workflow.invoke(initial_state)
        return {
            "response": result["final_response"],
            "pros": result["pros_found"]
        }
    except Exception as e:
        print(f"Error running agent: {e}")
        return {
            "response": "Sorry, I am having trouble connecting to the Matchmaker service.",
            "pros": []
        }
