import streamlit as st
import json
import datetime
import time
from src.rag_system import RAGSystem
from src.metrics import MetricsTracker
from src.logger import get_logger
from config.settings import config

logger = get_logger(__name__)

# Configure page
st.set_page_config(
    page_title=config.ui.page_title,
    layout=config.ui.layout,
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_system" not in st.session_state:
    with st.spinner("Loading AI Support System..."):
        st.session_state.rag_system = RAGSystem(config.knowledge_base_path)
if "metrics" not in st.session_state:
    st.session_state.metrics = MetricsTracker()

# Header
st.title("AI Customer Support")
st.markdown("*Professional support powered by AI technology*")

# Sidebar - Metrics Dashboard
with st.sidebar:
    st.header("Performance Dashboard")
    
    metrics_data = st.session_state.metrics.get_current_metrics()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", f"{metrics_data['accuracy']:.1f}%")
        st.metric("Total Queries", metrics_data['total_queries'])
    
    with col2:
        st.metric("Resolution Rate", f"{metrics_data['resolution_rate']:.1f}%")
        st.metric("Avg Response Time", f"{metrics_data['avg_response_time']:.2f}s")
    
    st.divider()
    
    # System Status
    st.subheader("System Status")
    st.success("AI System: Online")
    st.success("Knowledge Base: Loaded")
    st.success("API: Connected")
    
    st.divider()
    
    # Export Options
    st.subheader("Export Data")
    if st.button("Export Conversation"):
        if st.session_state.messages:
            conversation_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "messages": st.session_state.messages,
                "metrics": metrics_data
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(conversation_data, indent=2),
                file_name=f"conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("No conversation to export")
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Main Chat Interface
st.subheader("Customer Support Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show response details for assistant messages
        if message["role"] == "assistant" and "metadata" in message:
            with st.expander("Response Details"):
                metadata = message["metadata"]
                st.write(f"**Response Time:** {metadata['response_time']:.2f}s")
                st.write(f"**Confidence Score:** {metadata['confidence']:.2f}")
                st.write(f"**Sources Used:** {len(metadata['sources'])}")
                
                if metadata['sources']:
                    st.write("**Knowledge Sources:**")
                    for i, source in enumerate(metadata['sources'][:3], 1):
                        st.write(f"{i}. {source['title']} (Score: {source['score']:.2f})")

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            start_time = time.time()
            
            try:
                # Get response from RAG system
                response_data = st.session_state.rag_system.get_response(prompt)
                response_time = time.time() - start_time
                
                # Display response
                st.markdown(response_data["answer"])
                
                # Prepare metadata
                metadata = {
                    "response_time": response_time,
                    "confidence": response_data["confidence"],
                    "sources": response_data["sources"]
                }
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_data["answer"],
                    "metadata": metadata
                })
                
                # Track metrics
                st.session_state.metrics.add_interaction(
                    query=prompt,
                    response=response_data["answer"],
                    response_time=response_time,
                    confidence=response_data["confidence"],
                    sources_count=len(response_data["sources"])
                )
                
                logger.info("Successfully processed query with %.2f confidence", 
                           response_data["confidence"])
                
            except Exception as e:
                error_message = "I apologize, but I'm experiencing technical difficulties. Please try again later."
                st.error(error_message)
                logger.error("Error processing query: %s", str(e))
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message
                })

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <strong>AI Customer Support System v1.0</strong><br>
    Professional support powered by advanced AI technology<br>
    For complex issues, connect with our human support team
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    logger.info("Starting AI Customer Support System")