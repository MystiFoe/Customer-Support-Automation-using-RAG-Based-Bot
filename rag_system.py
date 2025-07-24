import os
import json
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from openai import OpenAI
from knowledge_base import KnowledgeBase

class RAGSystem:
    def __init__(self):
        """Initialize the RAG system with embeddings and vector database."""
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key"))
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = KnowledgeBase()
        self.index = None
        self.documents = []
        
        # Initialize the vector database
        self._initialize_vector_db()
    
    def _initialize_vector_db(self):
        """Initialize FAISS vector database with knowledge base documents."""
        try:
            # Load knowledge base
            self.documents = self.knowledge_base.get_all_documents()
            
            if not self.documents:
                raise Exception("No documents found in knowledge base")
            
            # Create embeddings for all documents
            texts = [doc['content'] for doc in self.documents]
            embeddings = self.embedding_model.encode(texts)
            
            # Initialize FAISS index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner Product for similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings.astype('float32'))
            self.index.add(embeddings.astype('float32'))
            
            print(f"✅ Vector database initialized with {len(self.documents)} documents")
            
        except Exception as e:
            print(f"❌ Error initializing vector database: {e}")
            raise
    
    def _retrieve_relevant_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve most relevant documents for the given query."""
        try:
            # Encode the query
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding.astype('float32'))
            
            # Search for similar documents
            scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
            
            # Return relevant documents with scores
            relevant_docs = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx != -1:  # Valid index
                    doc = self.documents[idx].copy()
                    doc['score'] = float(score)
                    relevant_docs.append(doc)
            
            return relevant_docs
            
        except Exception as e:
            print(f"❌ Error retrieving documents: {e}")
            return []
    
    def _generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate response using OpenAI with retrieved context."""
        try:
            # Prepare context from retrieved documents
            context = "\n\n".join([
                f"Source: {doc['title']}\nContent: {doc['content']}"
                for doc in context_docs
            ])
            
            # Construct the prompt
            system_prompt = """You are a helpful customer support AI assistant. Use the provided context to answer customer questions accurately and professionally. 

Guidelines:
- Provide clear, concise, and helpful answers
- Use information from the context when available
- If the context doesn't contain relevant information, politely indicate that you need to escalate to a human agent
- Be empathetic and understanding
- Maintain a professional but friendly tone
- If asked about technical issues, provide step-by-step solutions when possible"""

            user_prompt = f"""Context Information:
{context}

Customer Question: {query}

Please provide a helpful response based on the context above. If the context doesn't contain sufficient information to answer the question, let the customer know that you'll need to connect them with a human agent for further assistance."""

            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            
            # Calculate confidence based on context relevance
            confidence = self._calculate_confidence(context_docs)
            
            return {
                "answer": answer,
                "confidence": confidence,
                "sources": [
                    {
                        "title": doc["title"],
                        "score": doc["score"],
                        "category": doc.get("category", "General")
                    }
                    for doc in context_docs
                ]
            }
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return {
                "answer": "I apologize, but I'm experiencing technical difficulties. Please try again later or contact our human support team.",
                "confidence": 0.0,
                "sources": []
            }
    
    def _calculate_confidence(self, context_docs: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on retrieved documents relevance."""
        if not context_docs:
            return 0.0
        
        # Average of top document scores, weighted by position
        weights = [1.0, 0.7, 0.5]  # Give more weight to top results
        weighted_score = 0.0
        total_weight = 0.0
        
        for i, doc in enumerate(context_docs[:3]):
            weight = weights[i] if i < len(weights) else 0.3
            weighted_score += doc['score'] * weight
            total_weight += weight
        
        confidence = (weighted_score / total_weight) if total_weight > 0 else 0.0
        return min(1.0, max(0.0, confidence))  # Clamp between 0 and 1
    
    def get_response(self, query: str) -> Dict[str, Any]:
        """Main method to get RAG response for a user query."""
        try:
            # Step 1: Retrieve relevant documents
            relevant_docs = self._retrieve_relevant_documents(query, top_k=3)
            
            # Step 2: Generate response using retrieved context
            response_data = self._generate_response(query, relevant_docs)
            
            return response_data
            
        except Exception as e:
            print(f"❌ Error in RAG system: {e}")
            return {
                "answer": "I apologize, but I'm currently experiencing technical issues. Please try again later or contact our human support team for immediate assistance.",
                "confidence": 0.0,
                "sources": []
            }
    
    def add_to_knowledge_base(self, title: str, content: str, category: str = "General"):
        """Add new document to knowledge base and update vector index."""
        try:
            # Add to knowledge base
            new_doc = {
                "title": title,
                "content": content,
                "category": category
            }
            
            self.documents.append(new_doc)
            
            # Update vector index
            new_embedding = self.embedding_model.encode([content])
            faiss.normalize_L2(new_embedding.astype('float32'))
            self.index.add(new_embedding.astype('float32'))
            
            print(f"✅ Added new document to knowledge base: {title}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding document to knowledge base: {e}")
            return False
