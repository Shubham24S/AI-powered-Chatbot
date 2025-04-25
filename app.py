import streamlit as st
from src.chatbot import get_chatbot_response
from src.knowledge_base import load_knowledge_base
import time
import base64

# Page configuration
st.set_page_config(
    page_title="Insurance Policy Assistant",
    page_icon="💬",
    layout="wide"
)

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = ""
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

# Function to toggle chat visibility
def toggle_chat():
    st.session_state.show_chat = not st.session_state.show_chat

# Function to load local image
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        # Return placeholder if image not found
        return None

# Main app layout
if not st.session_state.show_chat:
    # Show welcome screen with image and chat bubble
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Use a placeholder image or your own image path
        image_path = "logo.png"  # Change this to your image path
        image_base64 = get_image_base64(image_path)
        
        if image_base64:
            image_html = f'<img src="data:image/png;base64,{image_base64}" class="welcome-image">'
        else:
            # Fallback to a placeholder if image can't be loaded
            image_html = '<img src="https://via.placeholder.com/200x150" class="welcome-image">'
        
        st.markdown(f"""
        <div class="welcome-container">
            {image_html}
            <h1>Welcome to Insurance Policy Assistant</h1>
            <p>Click the chat bubble in the bottom right corner to get started.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add chat bubble
    st.markdown("""
    <div class="chat-bubble" id="chat-bubble-clickable">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="24px" height="24px">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/>
            <path d="M7 9h10v2H7zm0-4h10v2H7zm0 8h5v2H7z"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a visible button that's positioned over the chat bubble
    st.button("Chat", key="toggle_chat_button", on_click=toggle_chat)
    
    # Add custom JavaScript to improve the click behavior
    st.markdown("""
    <script>
        // Wait for the page to load
        document.addEventListener('DOMContentLoaded', function() {
            // Get the chat bubble element
            const chatBubble = document.getElementById('chat-bubble-clickable');
            
            // Add click event listener
            if (chatBubble) {
                chatBubble.addEventListener('click', function() {
                    // Find the button
                    const buttons = document.querySelectorAll('button');
                    for (const button of buttons) {
                        if (button.innerText === 'Chat') {
                            button.click();
                            break;
                        }
                    }
                });
            }
        });
    </script>
    """, unsafe_allow_html=True)
else:
    # Show the full chat interface
    # Sidebar for document upload
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-header">
                <h2>📄 Insurance Documents</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        uploaded_files = st.file_uploader(
            "Upload insurance policy documents",
            type="pdf",
            accept_multiple_files=True,
            key="document_uploader"  # Added unique key for the uploader
        )
        
        if uploaded_files:
            with st.spinner("Processing documents..."):
                # Add a small delay for visual effect
                time.sleep(0.5)
                st.session_state.knowledge_base = load_knowledge_base(uploaded_files)
                st.success(f"{len(uploaded_files)} documents loaded successfully!")
        else:
            st.info("Please upload insurance policy documents to get started.")
        
        # Add visible minimize button in sidebar with proper styling
        st.markdown('<div class="minimize-button-container">', unsafe_allow_html=True)
        if st.button("Minimize Chat", key="minimize", use_container_width=True):
            toggle_chat()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat area
    st.markdown("""
    <div class="chat-header">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="30px" height="30px">
            <path d="M0 0h24v24H0V0z" fill="none"/>
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/>
            <path d="M7 9h10v2H7zm0-4h10v2H7zm0 8h5v2H7z"/>
        </svg>
        <h1>Insurance Policy Assistant</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    prompt = st.chat_input("Ask a question about insurance policies")
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
        
        # Get and display assistant response
        if st.session_state.knowledge_base:
            # Show typing animation
            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
            """, unsafe_allow_html=True)
            
            # Get response with a small delay for effect
            time.sleep(1)
            response = get_chatbot_response(prompt, st.session_state.knowledge_base)
            
            # Remove typing animation and show response
            typing_placeholder.empty()
            st.markdown(f'<div class="chat-message bot-message">{response}</div>', unsafe_allow_html=True)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            response = "Please upload insurance documents first so I can answer your questions."
            st.markdown(f'<div class="chat-message bot-message">{response}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})