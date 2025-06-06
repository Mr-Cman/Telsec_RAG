import streamlit as st
import time
from query_data import query_rag
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Telsec RAG Assistant",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Sophisticated, earthy styling inspired by the Garden palette
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Color palette variables */
    :root {
        --cream: #f5f2eb;
        --terracotta: #c8917a;
        --rust: #a67c6a;
        --chocolate: #4a2c2a;
        --sage: #6b8c6b;
        --forest: #3d4f3d;
        --warm-white: #faf8f3;
    }
    
    /* Global styling */
    .stApp {
        background-color: var(--cream);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 3rem 0 4rem 0;
        border-bottom: 2px solid var(--terracotta);
        margin-bottom: 3rem;
        background: linear-gradient(135deg, var(--warm-white) 0%, var(--cream) 100%);
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 600;
        color: var(--chocolate);
        margin: 0;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(74, 44, 42, 0.1);
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        color: var(--rust);
        margin-top: 0.75rem;
        font-weight: 400;
        font-style: italic;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, var(--sage) 0%, #7a9b7a 100%);
        color: var(--warm-white);
        padding: 1.25rem 1.75rem;
        margin: 1.5rem 0;
        border-radius: 0 16px 16px 16px;
        box-shadow: 0 4px 12px rgba(107, 140, 107, 0.25);
        border-left: 4px solid var(--forest);
    }
    
    .user-message-text {
        color: var(--warm-white);
        font-size: 1.05rem;
        margin: 0;
        font-weight: 500;
        line-height: 1.5;
    }
    
    .assistant-message {
        background-color: var(--warm-white);
        border: 2px solid var(--terracotta);
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(200, 145, 122, 0.15);
        position: relative;
    }
    
    .assistant-message::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, var(--terracotta), var(--rust));
        border-radius: 16px;
        z-index: -1;
    }
    
    .assistant-message-text {
        color: var(--chocolate);
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 0;
        white-space: pre-wrap;
    }
    
    .sources-section {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--terracotta);
    }
    
    .sources-title {
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--chocolate);
        margin-bottom: 0.75rem;
    }
    
    .source-item {
        background: linear-gradient(135deg, var(--cream) 0%, #f0ebe0 100%);
        border-left: 3px solid var(--sage);
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: var(--forest);
        font-weight: 500;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border: 2px solid var(--terracotta);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        font-size: 1.05rem;
        background-color: var(--warm-white);
        color: var(--chocolate);
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--sage);
        outline: none;
        box-shadow: 0 0 0 3px rgba(107, 140, 107, 0.2);
        background-color: #ffffff;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--rust);
        font-style: italic;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--sage) 0%, var(--forest) 100%);
        color: var(--warm-white);
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
        width: 100%;
        font-family: 'Playfair Display', serif;
        letter-spacing: 0.02em;
        box-shadow: 0 4px 12px rgba(107, 140, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(107, 140, 107, 0.4);
        background: linear-gradient(135deg, #7a9b7a 0%, var(--sage) 100%);
    }
    
    /* Loading state */
    .loading-message {
        background: linear-gradient(135deg, var(--warm-white) 0%, var(--cream) 100%);
        border: 2px solid var(--terracotta);
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 16px;
        text-align: center;
        color: var(--rust);
        box-shadow: 0 4px 12px rgba(200, 145, 122, 0.15);
    }
    
    .typing-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--sage);
        margin: 0 2px;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-indicator:nth-child(1) { animation-delay: -0.32s; }
    .typing-indicator:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { 
            transform: scale(0.8);
            opacity: 0.5;
        } 
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .loading-text {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        margin-left: 1rem;
        color: var(--chocolate);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--terracotta), transparent);
        margin: 2rem 0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--cream);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--terracotta);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--rust);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">Telsec RAG Assistant</h1>
        <p class="main-subtitle">Ask questions about lease agreements and property documents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display conversation history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <p class="user-message-text">{message["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            display_assistant_message(message["content"], message.get("sources", []))
    
    # Input area
    st.markdown("---")
    
    # Use form to handle input properly
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "",
                placeholder="Ask about lease terms, rent calculations, insurance requirements...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.form_submit_button("Send", type="primary")
    
    # Handle form submission
    if send_button and user_input:
        handle_user_input(user_input)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_user_input(user_input):
    """Process user input and get RAG response"""
    
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input
    })
    
    # Show loading state temporarily
    with st.container():
        st.markdown("""
        <div class="loading-message">
            <span class="typing-indicator"></span>
            <span class="typing-indicator"></span>
            <span class="typing-indicator"></span>
            <span class="loading-text">Searching through lease documents...</span>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Get response from RAG system
            response_text = query_rag(user_input)
            
            # Parse response to extract sources
            if "Sources:" in response_text:
                response_parts = response_text.split("Sources:")
                clean_response = response_parts[0].replace("Response:", "").strip()
                sources_text = response_parts[1].strip()
                sources = [s.strip().strip("[]'\"") for s in sources_text.split(",") if s.strip() and s.strip() != "None"]
            else:
                clean_response = response_text.replace("Response:", "").strip()
                sources = []
            
            # Add assistant response to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": clean_response,
                "sources": sources
            })
            
        except Exception as e:
            # Add error message to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"I apologize, but I encountered an error while processing your request: {str(e)}",
                "sources": []
            })

def display_assistant_message(content, sources):
    """Display an assistant message with sources"""
    
    sources_html = ""
    if sources and any(source and source != "None" for source in sources):
        valid_sources = [source for source in sources if source and source != "None"]
        if valid_sources:
            sources_html = f"""
            <div class="sources-section">
                <div class="sources-title">Sources</div>
                {"".join([f'<div class="source-item">{source}</div>' for source in valid_sources])}
            </div>
            """
    
    st.markdown(f"""
    <div class="assistant-message">
        <p class="assistant-message-text">{content}</p>
        {sources_html}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 