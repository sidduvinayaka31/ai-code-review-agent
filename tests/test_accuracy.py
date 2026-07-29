import os
import sys

# Add the root directory to sys.path so we can import from agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import build_graph

def test_samples():
    print("=====================================")
    print("Running Milestone 2 Accuracy Validation")
    print("=====================================\n")
    
    app_graph = build_graph()
    samples_dir = os.path.join(os.path.dirname(__file__), "samples")
    
    for filename in os.listdir(samples_dir):
        if not filename.endswith(".py") and not filename.endswith(".java"):
            continue
            
        filepath = os.path.join(samples_dir, filename)
        print(f"Testing file: {filename}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
            
        final_state = app_graph.invoke({"code": code})
        
        print(f"Detected Language: {final_state.get('language')}")
        
        if not final_state.get("syntax_valid", True):
            print(f"Syntax Error: {final_state.get('syntax_error')}\n")
            continue
            
        findings = final_state.get("final_report", [])
        print(f"Total Issues Found: {len(findings)}")
        
        for idx, finding in enumerate(findings, 1):
            print(f"  {idx}. [{finding.severity}] {finding.issue_type} (Line: {finding.line_number})")
            print(f"     Description: {finding.description}")
        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    test_samples()
