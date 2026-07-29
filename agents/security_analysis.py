import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from agents.state import AgentState, AnalysisOutput
from rag.knowledge_base import get_retriever

def analyze_security_vulnerabilities(state: AgentState) -> dict:
    """Scans code for security vulnerabilities using RAG context."""
    code = state.get("code", "")
    language = state.get("language", "Unknown")
    
    if language == "Unknown":
        return {"security_findings": []}
        
    print(f"--- Running Security Analysis on {language} code ---")
    
    try:
        # 1. Retrieve relevant security context from ChromaDB based on the code
        retriever = get_retriever()
        docs = retriever.invoke(code)
        context = "\n\n".join([d.page_content for d in docs])
        
        # 2. Initialize LLM
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
        structured_llm = llm.with_structured_output(AnalysisOutput)
        
        prompt = PromptTemplate.from_template(
            """You are an expert Security Engineer and Code Reviewer.
            Analyze the following {language} code specifically for Security Vulnerabilities.
            Use the provided context (which includes OWASP standards and best practices) to identify issues.
            
            Context from Knowledge Base:
            {context}
            
            Code to analyze:
            ```{language}
            {code}
            ```
            
            Classify findings by type (e.g., 'SQL Injection', 'Cross-Site Scripting') and severity ('High', 'Medium', 'Low').
            Provide specific line numbers or functions where the vulnerability exists in the line_number field.
            If there are no security vulnerabilities, return an empty list of findings.
            """
        )
        
        chain = prompt | structured_llm
        result = chain.invoke({"language": language, "code": code, "context": context})
        
        findings = result.findings if result and hasattr(result, 'findings') else []
        return {"security_findings": findings}
        
    except Exception as e:
        print(f"Security analysis failed: {repr(e)}")
        return {"security_findings": [], "security_analysis_error": f"Security Analysis Error: {repr(e)}"}
