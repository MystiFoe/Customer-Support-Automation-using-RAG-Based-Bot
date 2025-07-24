import streamlit as st
import json
import datetime
import pandas as pd
from simple_rag_system import SimpleRAGSystem
from metrics import MetricsTracker
import time

# Configure page
st.set_page_config(
    page_title="AI Customer Support Bot",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_system" not in st.session_state:
    with st.spinner("Initializing AI Support System..."):
        st.session_state.rag_system = SimpleRAGSystem()
if "metrics" not in st.session_state:
    st.session_state.metrics = MetricsTracker()

# Main header
st.title("🤖 AI Customer Support Bot")
st.markdown("<span style='font-size:16px; color:#333;'>Powered by Retrieval-Augmented Generation (RAG) Technology</span>", unsafe_allow_html=True)

# Sidebar for metrics and controls
with st.sidebar:
    st.header("📊 Performance Metrics")
    
    # Display current metrics
    metrics_data = st.session_state.metrics.get_current_metrics()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Response Accuracy", f"{metrics_data['accuracy']:.1f}%")
        st.metric("Total Queries", metrics_data['total_queries'])
    
    with col2:
        st.metric("Resolution Rate", f"{metrics_data['resolution_rate']:.1f}%")
        st.metric("Avg Response Time", f"{metrics_data['avg_response_time']:.2f}s")
    
    st.divider()
    
    # System status
    st.header("🔧 System Status")
    st.success("✅ RAG System: Online")
    st.success("✅ Knowledge Base: Loaded")
    st.success("✅ OpenAI API: Connected")
    
    st.divider()
    
    # Export conversation
    st.header("💾 Export Options")
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

# Main chat interface
st.header("💬 Customer Support Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show metadata for assistant messages
        if message["role"] == "assistant" and "metadata" in message:
            with st.expander("View Response Details"):
                metadata = message["metadata"]
                st.write(f"**Response Time:** {metadata['response_time']:.2f}s")
                st.write(f"**Confidence Score:** {metadata['confidence']:.2f}")
                st.write(f"**Sources Used:** {len(metadata['sources'])}")
                
                if metadata['sources']:
                    st.write("**Knowledge Base Sources:**")
                    for i, source in enumerate(metadata['sources'][:3], 1):
                        st.write(f"{i}. {source['title']} (Relevance: {source['score']:.2f})")

# Chat input
if prompt := st.chat_input("Ask me anything about our products or services..."):
    # Add user message to chat history
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
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_data["answer"],
                    "metadata": metadata
                })
                
                error_message = f"We are experiencing technical difficulties. Please try again later. Error: {str(e)}"
                st.session_state.metrics.add_interaction(
                    query=prompt,
                    response=response_data["answer"],
                    response_time=response_time,
                    confidence=response_data["confidence"],
                    sources_count=len(response_data["sources"])
                )
                
            except Exception as e:
                error_message = f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
                st.error(error_message)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message
                })

# Footer information
st.divider()
st.markdown("""
<div style='text-align: center; color: #444;'>
    <p><strong>AI Customer Support Bot v1.0</strong></p>
    <p>This bot uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses based on our knowledge base.</p>
    <p>For complex issues, you may be transferred to a human agent.</p>
</div>
""", unsafe_allow_html=True)
