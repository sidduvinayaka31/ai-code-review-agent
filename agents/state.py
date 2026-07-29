from typing import TypedDict, List
from pydantic import BaseModel, Field

# Pydantic models for structured output
class Finding(BaseModel):
    issue_type: str = Field(description="The category of the issue (e.g., 'Code Smell', 'Security Vulnerability', 'Anti-Pattern')")
    severity: str = Field(description="The severity level: 'High', 'Medium', or 'Low'")
    line_number: str = Field(description="The approximate line number or function name where the issue occurs, or 'Global' if it applies to the whole file")
    description: str = Field(description="A detailed explanation of the finding and why it is an issue")
    recommendation: str = Field(description="Actionable advice on how to fix or mitigate the issue")

class AnalysisOutput(BaseModel):
    findings: List[Finding]

# State definition for LangGraph
class AgentState(TypedDict):
    code: str
    language: str  # 'Python', 'Java', or 'Unknown'
    syntax_valid: bool
    syntax_error: str
    code_analysis_findings: List[Finding]
    security_findings: List[Finding]
    final_report: List[Finding]
    code_analysis_error: str
    security_analysis_error: str
