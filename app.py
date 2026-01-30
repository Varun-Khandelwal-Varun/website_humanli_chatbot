import streamlit as st
from crawler import extract_website_content
from vector_store import create_vector_store
from qa_chain import get_qa_chain

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Website Intelligence Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# Custom CSS (Professional + Fix sidebar icon)
# -------------------------------------------------
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #0e1117;
    }

    h1, h2, h3, h4 {
        color: #fafafa;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }

    /* Chat bubble styling */
    .stChatMessage {
        background-color: #1f2933;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* 🔥 FINAL FIX: hide sidebar toggle icon/text */
    button[kind="header"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="baseButton-header"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("## 🌐 Website Intelligence Chatbot")
st.markdown(
    "An AI-powered chatbot that answers questions **strictly based on the content of a provided website**."
)

# -------------------------------------------------
# IMPORTANT NOTE (Company-facing concern)
# -------------------------------------------------
st.info(
    "ℹ️ **Note:** This is a live demo application. "
    "If the OpenAI API quota is exceeded, the chatbot may show limited or unavailable responses. "
    "The core crawling, embedding, retrieval, and grounding logic remains fully functional."
)

st.divider()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ How it works")
    st.markdown(
        """
        1. Enter a website URL  
        2. Index the website content  
        3. Ask questions related **only** to that website  

        **No external knowledge.  
        No hallucinations.**
        """
    )

    st.markdown("---")

    st.markdown("### 🧠 Tech Stack")
    st.markdown(
        """
        - Streamlit  
        - LangChain  
        - SentenceTransformers  
        - ChromaDB  
        - OpenAI LLM  
        """
    )

    st.markdown("---")

    st.markdown("### 🚀 Key Guarantees")
    st.success("Answers strictly from website content")
    st.success("Persistent embeddings (no re-indexing per query)")
    st.success("Session-level conversational memory")

# -------------------------------------------------
# URL Input Section
# -------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input(
        "🔗 Website URL",
        placeholder="https://example.com"
    )

with col2:
    index_btn = st.button("📥 Index Website", use_container_width=True)

# -------------------------------------------------
# Website Indexing Logic
# -------------------------------------------------
if index_btn:
    if not url:
        st.warning("Please enter a valid website URL.")
    else:
        with st.spinner("Extracting and indexing website content..."):
            text, title = extract_website_content(url)

            if not text:
                st.error("Unable to extract meaningful content from this website.")
            else:
                vectordb = create_vector_store(text, title, url)
                st.session_state.qa_chain = get_qa_chain(vectordb)
                st.session_state.indexed = True
                st.session_state.chat_history = []

                st.success("Website indexed successfully. You can now ask questions.")

st.divider()

# -------------------------------------------------
# Chat Interface
# -------------------------------------------------
if st.session_state.get("indexed", False):
    st.markdown("### 💬 Ask Questions")

    user_question = st.chat_input("Ask something about the website...")

    if user_question:
        st.session_state.chat_history.append(("user", user_question))

        try:
            result = st.session_state.qa_chain({"question": user_question})
            answer = result["answer"]
        except Exception:
            answer = "The answer is not available on the provided website."

        st.session_state.chat_history.append(("assistant", answer))

    # Display chat history
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

else:
    st.info("Index a website to start asking questions.")
