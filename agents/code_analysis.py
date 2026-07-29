import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from agents.state import AgentState, AnalysisOutput

def analyze_code_quality(state: AgentState) -> dict:
    """Analyzes the code for smells, complexity, and anti-patterns."""
    code = state.get("code", "")
    language = state.get("language", "Unknown")
    
    if language == "Unknown":
        return {"code_analysis_findings": [], "code_analysis_error": "Cannot analyze unknown language."}
        
    print(f"--- Running Code Analysis on {language} code ---")
    
    try:
        # Initialize the LLM
        # Using Groq — free tier, very fast, no quota issues
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
        
        # Enforce structured output matching our Pydantic model
        structured_llm = llm.with_structured_output(AnalysisOutput)
        
        prompt = PromptTemplate.from_template(
            """You are an expert Software Engineer and Code Reviewer.
            Analyze the following {language} code for:
            - Code Smells
            - Complexity Issues
            - Design Anti-Patterns
            - Poor Coding Practices
            
            Do NOT focus on security vulnerabilities (another agent handles that).
            Be critical but constructive. Score severity as 'High', 'Medium', or 'Low'.
            
            Code to analyze:
            ```{language}
            {code}
            ```
            """
        )
        
        chain = prompt | structured_llm
        result = chain.invoke({"language": language, "code": code})
        
        # Ensure we return a list of findings, even if it's empty
        findings = result.findings if result and hasattr(result, 'findings') else []
        return {"code_analysis_findings": findings}
        
    except Exception as e:
        print(f"Code analysis failed: {repr(e)}")
        # Optionally fallback to a basic model or just return the error
        return {"code_analysis_findings": [], "code_analysis_error": f"Code Analysis Error: {repr(e)}"}
