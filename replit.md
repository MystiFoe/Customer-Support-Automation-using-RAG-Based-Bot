# AI Customer Support Bot - replit.md

## Overview

This is an AI-powered customer support bot built with Streamlit that uses RAG (Retrieval-Augmented Generation) technology to provide intelligent responses to customer queries. The system combines a knowledge base with vector similarity search and OpenAI's language models to deliver accurate, contextual support responses.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit web interface providing an interactive chat experience
- **RAG Engine**: Core retrieval-augmented generation system using sentence transformers and FAISS
- **Knowledge Management**: JSON-based document storage with categorization
- **Metrics Tracking**: Performance monitoring and analytics system
- **Vector Database**: FAISS-powered similarity search for document retrieval

## Key Components

### 1. Main Application (app.py)
- **Purpose**: Streamlit frontend providing the user interface
- **Key Features**: 
  - Chat interface for customer interactions
  - Real-time metrics display in sidebar
  - Session state management for conversation history
- **Architecture Decision**: Streamlit chosen for rapid prototyping and built-in state management

### 2. RAG System (rag_system.py)
- **Purpose**: Core AI engine combining retrieval and generation
- **Key Features**:
  - Sentence transformer embeddings (all-MiniLM-L6-v2)
  - FAISS vector database for similarity search
  - OpenAI API integration for response generation
- **Architecture Decision**: FAISS selected for efficient similarity search with cosine similarity scoring

### 3. Knowledge Base (knowledge_base.py)
- **Purpose**: Document storage and retrieval system
- **Key Features**:
  - JSON-based document storage
  - Category-based organization
  - Search functionality by keywords
- **Architecture Decision**: JSON chosen for simplicity and human-readable format, suitable for small to medium knowledge bases

### 4. Metrics Tracker (metrics.py)
- **Purpose**: Performance monitoring and analytics
- **Key Features**:
  - Response time tracking
  - Confidence scoring
  - Resolution rate estimation
  - Accuracy metrics
- **Architecture Decision**: In-memory tracking suitable for demo/development, can be extended to persistent storage

## Data Flow

1. **User Query**: Customer submits question through Streamlit interface
2. **Embedding**: Query converted to vector using sentence transformer
3. **Retrieval**: FAISS searches for most relevant documents using cosine similarity
4. **Context Building**: Top relevant documents combined with query
5. **Generation**: OpenAI API generates response using retrieved context
6. **Metrics**: Interaction logged with performance data
7. **Response**: Answer displayed to user with confidence indicators

## External Dependencies

### AI/ML Libraries
- **sentence-transformers**: For text embeddings
- **faiss-cpu**: Vector similarity search
- **openai**: GPT API integration
- **numpy**: Numerical operations

### Web Framework
- **streamlit**: Frontend framework
- **pandas**: Data manipulation for metrics

### System Requirements
- **OpenAI API Key**: Required for response generation
- **Python 3.8+**: Runtime environment

## Deployment Strategy

### Current Setup
- **Local Development**: Streamlit dev server
- **Data Storage**: Local JSON files
- **State Management**: Streamlit session state

### Production Considerations
- **Scaling**: Consider moving to proper vector database (Pinecone, Weaviate)
- **Storage**: Migrate from JSON to proper database (PostgreSQL with pgvector)
- **Caching**: Implement Redis for embedding caching
- **Monitoring**: Add proper logging and error tracking
- **Security**: Environment variable management for API keys

### Key Architectural Decisions

1. **RAG vs Fine-tuning**: Chose RAG for flexibility and ability to update knowledge without retraining
2. **FAISS vs Cloud Vector DB**: Selected FAISS for simplicity and local development, easily upgradeable to cloud solutions
3. **JSON vs Database**: JSON selected for initial implementation due to simplicity, with clear migration path to proper database
4. **Streamlit vs FastAPI**: Streamlit chosen for rapid prototyping and built-in UI components
5. **Local vs Cloud Embeddings**: Using local sentence-transformers for cost efficiency and reduced latency

The architecture is designed to be easily extensible, with clear interfaces between components allowing for future enhancements like database integration, advanced analytics, and scalable deployment.