import streamlit as st
import os
from utils.syntax_validator import validate_code

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
Welcome to the Developer Portal. Submit your Python or Java code below for an automated review of structure, code smells, and security vulnerabilities.
""")

st.header("Code Submission")

# Language selection
language = st.selectbox("Select Language", ["Python", "Java"])

# Submission Method
submission_method = st.radio("Choose submission method:", ["Paste Code", "Upload File"])

code_input = ""
run_btn = False

if submission_method == "Paste Code":
    # Moving the button next to the text area
    col1, col2 = st.columns([5, 1])
    with col1:
        code_input = st.text_area(f"Paste your {language} code here:", height=300)
    with col2:
        # Push button to the bottom to align with the text area
        st.markdown("<div style='margin-top: 275px;'></div>", unsafe_allow_html=True)
        run_btn = st.button("Run syntax validation", type="primary", use_container_width=True)
else:
    uploaded_file = st.file_uploader(f"Upload {language} file", type=["py", "java"])
    if uploaded_file is not None:
        # Check extension against selected language
        ext = uploaded_file.name.split('.')[-1]
        if (language == "Python" and ext != "py") or (language == "Java" and ext != "java"):
            st.error(f"File extension .{ext} does not match selected language {language}.")
        else:
            code_input = uploaded_file.getvalue().decode("utf-8")
            st.text_area("File Contents:", value=code_input, height=300, disabled=True)
    
    run_btn = st.button("Run syntax validation", type="primary")

if run_btn:
    st.header("Analysis")
    if not code_input.strip():
        st.warning("Please provide some code to validate.")
    else:
        with st.spinner(f"Validating {language} syntax..."):
            is_valid, message = validate_code(code_input, language)
            
            if is_valid:
                st.markdown(f'<p class="success-text">✅ {message}</p>', unsafe_allow_html=True)
                st.info("Syntax is valid. The code is ready for AI multi-agent analysis.")
            else:
                st.markdown(f'<p class="error-text">❌ {message}</p>', unsafe_allow_html=True)
                st.error("Please fix syntax errors before proceeding to AI analysis.")


