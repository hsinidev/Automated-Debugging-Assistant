import streamlit as st
import ollama

# --- Configuration ---
OLLAMA_MODEL = 'llama3:8b'
DEV_INFO = "powrd by Hsini Mohame (hsini.web@gmail.com)"

# Force the layout and title
st.set_page_config(
    page_title="AI Debugging Assistant",
    layout="wide",
)

st.title("?? Automated Debugging Assistant")
st.subheader("Analyze Error Messages and Get Precise Fixes")
st.caption(DEV_INFO)
st.markdown("---")

# --- Debugging Logic ---

def analyze_traceback(code_block, traceback):
    # This System Prompt is the CRITICAL part of the Agent's logic
    system_prompt = (
        f"You are a Senior Software Debugging Expert. Your task is to analyze the provided code and traceback "
        f"and provide a three-part structured response ONLY. "
        f"1. A section titled 'Root Cause:' explaining the exact reason for the error. "
        f"2. A section titled 'Line of Fix:' indicating the specific line number and file. "
        f"3. A section titled 'Suggested Code Fix:' providing the corrected, complete code block using markdown syntax."
        f"Be concise, professional, and accurate."
    )
    
    user_prompt = (
        "Analyze the following:\n\n"
        f"### CODE TO ANALYZE:\n{code_block}\n\n"
        f"### TRACEBACK/ERROR MESSAGE:\n{traceback}\n"
    )
    
    try:
        response = ollama.generate(
            model=OLLAMA_MODEL, 
            prompt=user_prompt,
            system=system_prompt
        )
        return response['response']
        
    except Exception as e:
        return f"Error connecting to Ollama: {e}. Ensure the service is running and model '{OLLAMA_MODEL}' is pulled."


# --- UI Interface ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 1. Paste the Source Code")
    code_input = st.text_area(
        "Source Code",
        height=300,
        placeholder="Paste your full code block here..."
    )

with col2:
    st.markdown("#### 2. Paste the Error Traceback")
    traceback_input = st.text_area(
        "Traceback/Error Message",
        height=300,
        placeholder="Paste the full error traceback here..."
    )

st.markdown("---")

if st.button("Analyze and Fix Code", type="primary", use_container_width=True):
    if code_input and traceback_input:
        with st.spinner("Analyzing traceback and formulating fix..."):
            debug_output = analyze_traceback(code_input, traceback_input)
            
        st.subheader("? Debugging Report")
        st.info(f"Analysis performed by {OLLAMA_MODEL}.")
        st.markdown(debug_output)
    else:
        st.error("Please provide both the Source Code and the Error Traceback.")