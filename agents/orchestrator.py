from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from agents.state import AgentState
from agents.code_analysis import analyze_code_quality
from agents.security_analysis import analyze_security_vulnerabilities
from utils.syntax_validator import validate_code

class LanguageDetectionOutput(BaseModel):
    language: str = Field(description="The detected programming language. Must be 'Python', 'Java', or 'Unknown'")

def detect_language(state: AgentState) -> dict:
    """Detects the programming language of the given code."""
    code = state.get("code", "")
    print("--- Detecting Language ---")
    
    # Fast heuristics first for speed
    if "public class" in code or "public static void main" in code or "import java." in code:
        return {"language": "Java"}
    if "def " in code and ":" in code or "import sys" in code or "import os" in code:
        return {"language": "Python"}
        
    # Fallback to LLM for tricky cases
    try:
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
        structured_llm = llm.with_structured_output(LanguageDetectionOutput)
        result = structured_llm.invoke(f"What programming language is this code?\n\n{code}")
        
        lang = result.language
        if lang not in ["Python", "Java"]:
            lang = "Unknown"
        return {"language": lang}
    except Exception as e:
        print(f"Language detection failed: {e}")
        return {"language": "Unknown"}

def validate_syntax(state: AgentState) -> dict:
    """Validates the syntax of the code before analysis."""
    print("--- Validating Syntax ---")
    code = state.get("code", "")
    language = state.get("language", "Unknown")
    
    if language == "Unknown":
        return {"syntax_valid": False, "syntax_error": "Cannot validate syntax of unknown language."}
        
    is_valid, msg = validate_code(code, language)
    return {"syntax_valid": is_valid, "syntax_error": msg if not is_valid else ""}

def merge_findings(state: AgentState) -> dict:
    """Merges findings from all agents into a unified report."""
    print("--- Merging Findings ---")
    code_findings = state.get("code_analysis_findings", [])
    security_findings = state.get("security_findings", [])
    
    # Combine lists
    final_report = security_findings + code_findings
    return {"final_report": final_report}

def build_graph():
    """Builds and returns the LangGraph orchestrator."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("detect_language", detect_language)
    workflow.add_node("validate_syntax", validate_syntax)
    workflow.add_node("analyze_code", analyze_code_quality)
    workflow.add_node("analyze_security", analyze_security_vulnerabilities)
    workflow.add_node("merge_findings", merge_findings)
    
    # Define edges
    workflow.add_edge(START, "detect_language")
    workflow.add_edge("detect_language", "validate_syntax")
    
    # Conditional routing after syntax validation
    def route_after_syntax(state: AgentState):
        if state.get("syntax_valid"):
            return ["analyze_code", "analyze_security"]
        return ["merge_findings"]
        
    workflow.add_conditional_edges(
        "validate_syntax",
        route_after_syntax,
        ["analyze_code", "analyze_security", "merge_findings"]
    )
    
    # Fan in (Merge results once both are done)
    workflow.add_edge("analyze_code", "merge_findings")
    workflow.add_edge("analyze_security", "merge_findings")
    
    workflow.add_edge("merge_findings", END)
    
    # Compile the graph
    app = workflow.compile()
    return app
