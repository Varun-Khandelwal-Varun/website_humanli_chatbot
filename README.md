# Website-Based Chatbot (Humanli.ai Assignment)

## Architecture

### 1. Crawling Strategy
- **Tool**: Trafilatura + BeautifulSoup
- **Logic**: Extracts main content while removing headers, footers, navigation, and ads using trafilatura's intelligent extraction
- **Deduplication**: MD5 hashing of content to avoid storing duplicate pages
- **Scope**: Stays within same domain, excludes static files

### 2. Text Processing
- **Chunking**: RecursiveCharacterTextSplitter with configurable size/overlap
- **Strategy**: Semantic chunking using natural separators (paragraphs → sentences → words)
- **Metadata**: Preserves source URL, page title, and chunk index

### 3. Embeddings & Vector DB
- **Model**: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
  - **Why**: Lightweight, fast, good semantic understanding, runs locally
- **Database**: ChromaDB (persistent)
  - **Why**: Open-source, local storage, no external dependencies, efficient similarity search

### 4. LLM Configuration
- **Primary**: OpenAI GPT-3.5-Turbo via API
  - **Why**: Reliable, fast, good instruction following for strict constraints
- **Alternative**: Ollama (Mistral) for local execution
  - **Why**: Privacy, no API costs, works offline

### 5. Conversation Memory
- **Implementation**: ConversationBufferMemory (LangChain)
- **Scope**: Session-based, cleared when new URL is indexed
- **Function**: Maintains context across follow-up questions

## Setup Instructions

1. **Clone Repository**
   ```bash
   git clone &lt;repo-url&gt;
   cd website-chatbot# humanli_chatbot
# humanli_chatbot
# humanli_chatbot
