import streamlit as st
import os
from agents.orchestrator import build_graph

# Configure Streamlit page
st.set_page_config(
    page_title="AI Code Review & Security Analysis Agent",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: monospace;
        font-size: 14px;
    }
    .success-text {
        color: #00cc66;
        font-weight: bold;
    }
    .error-text {
        color: #ff4b4b;
        font-weight: bold;
    }
    /* Style for the button to make text dark like the mockup */
    .stButton > button[kind="primary"] {
        color: #000000 !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI Code Review & Security Analysis Agent")
st.markdown("""
Welcome to the Developer Portal. Submit your Python or Java code below for an automated, multi-agent review of structure, code smells, and security vulnerabilities.
""")

st.header("Code Submission")

# Submission Method
submission_method = st.radio("Choose submission method:", ["Paste Code", "Upload File"])

code_input = ""
run_btn = False

if submission_method == "Paste Code":
    col1, col2 = st.columns([5, 1])
    with col1:
        code_input = st.text_area("Paste your Python or Java code here (Language Auto-Detected):", height=300)
    with col2:
        st.markdown("<div style='margin-top: 275px;'></div>", unsafe_allow_html=True)
        run_btn = st.button("Run AI Analysis", type="primary", use_container_width=True)
else:
    uploaded_file = st.file_uploader("Upload Python or Java file", type=["py", "java"])
    if uploaded_file is not None:
        code_input = uploaded_file.getvalue().decode("utf-8")
        st.text_area("File Contents:", value=code_input, height=300, disabled=True)
    
    run_btn = st.button("Run AI Analysis", type="primary")

if run_btn:
    st.header("Analysis Results")
    if not code_input.strip():
        st.warning("Please provide some code to validate.")
    else:
        with st.spinner("Initializing AI Agents... (Detecting language, running Code & Security Analysis in parallel)"):
            app_graph = build_graph()
            
            try:
                # Run the graph
                final_state = app_graph.invoke({"code": code_input})
                
                detected_language = final_state.get("language", "Unknown")
                
                if detected_language == "Unknown":
                    st.error("❌ Could not detect the programming language. Please ensure it is valid Python or Java code.")
                else:
                    st.success(f"✅ Language Detected: **{detected_language}**")
                    
                    if not final_state.get("syntax_valid", True):
                        st.error(f"❌ Syntax Error Detected:\n{final_state.get('syntax_error', '')}")
                        st.warning("Analysis skipped due to invalid syntax. Please fix the syntax errors and try again.")
                    else:
                        # Display any agent errors
                        code_err = final_state.get("code_analysis_error", "")
                        sec_err = final_state.get("security_analysis_error", "")
                        
                        if code_err:
                            st.error(f"⚠️ {code_err}")
                        if sec_err:
                            st.error(f"⚠️ {sec_err}")
                            
                        findings = final_state.get("final_report", [])
                        
                        if not findings:
                            st.balloons()
                            st.success("Wow! No code smells, anti-patterns, or security vulnerabilities found! Fantastic job! 🎉")
                        else:
                            st.subheader(f"Total Issues Found: {len(findings)}")
                            
                            # Sort findings by severity: High -> Medium -> Low
                            severity_map = {"High": 0, "Medium": 1, "Low": 2}
                            findings.sort(key=lambda x: severity_map.get(x.severity, 3))
                            
                            # Display nicely in Streamlit Expanders
                            for f in findings:
                                icon = "🔴" if f.severity == "High" else "🟡" if f.severity == "Medium" else "🔵"
                                with st.expander(f"{icon} **{f.severity} Severity:** {f.issue_type} (Location: {f.line_number})"):
                                    st.markdown(f"**Description:**\n{f.description}")
                                    st.markdown(f"**Recommendation:**\n{f.recommendation}")
                                
            except Exception as e:
                st.error(f"An error occurred during multi-agent analysis: {e}")
