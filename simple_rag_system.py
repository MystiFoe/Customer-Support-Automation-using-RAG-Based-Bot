import os
import json
from typing import List, Dict, Any
import re
from openai import OpenAI
from knowledge_base import KnowledgeBase

class SimpleRAGSystem:
    def __init__(self):
        """Initialize a simple RAG system using keyword matching instead of embeddings."""
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.knowledge_base = KnowledgeBase()
        self.documents = []
        
        # Initialize the document store
        self._initialize_document_store()
    
    def _initialize_document_store(self):
        """Initialize document store with knowledge base documents."""
        try:
            # Load knowledge base
            self.documents = self.knowledge_base.get_all_documents()
            
            if not self.documents:
                raise Exception("No documents found in knowledge base")
            
            print(f"✅ Document store initialized with {len(self.documents)} documents")
            
        except Exception as e:
            print(f"❌ Error initializing document store: {e}")
            raise
    
    def _retrieve_relevant_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve most relevant documents using keyword matching and scoring."""
        try:
            query_lower = query.lower()
            query_words = set(re.findall(r'\w+', query_lower))
            
            scored_docs = []
            
            for doc in self.documents:
                # Calculate relevance score based on keyword matching
                title_lower = doc.get('title', '').lower()
                content_lower = doc.get('content', '').lower()
                category_lower = doc.get('category', '').lower()
                
                # Extract words from document
                title_words = set(re.findall(r'\w+', title_lower))
                content_words = set(re.findall(r'\w+', content_lower))
                category_words = set(re.findall(r'\w+', category_lower))
                
                # Calculate scores
                title_score = len(query_words.intersection(title_words)) * 3  # Higher weight for title matches
                content_score = len(query_words.intersection(content_words)) * 1
                category_score = len(query_words.intersection(category_words)) * 2
                
                # Bonus for exact phrase matches
                phrase_bonus = 0
                for word in query_words:
                    if word in content_lower:
                        phrase_bonus += 1
                    if word in title_lower:
                        phrase_bonus += 2
                
                total_score = title_score + content_score + category_score + phrase_bonus
                
                if total_score > 0:
                    doc_copy = doc.copy()
                    doc_copy['score'] = total_score / max(len(query_words), 1)  # Normalize by query length
                    scored_docs.append(doc_copy)
            
            # Sort by score and return top_k
            scored_docs.sort(key=lambda x: x['score'], reverse=True)
            return scored_docs[:top_k]
            
        except Exception as e:
            print(f"❌ Error retrieving documents: {e}")
            return []
    
    def _generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate response using OpenAI with retrieved context."""
        try:
            # Prepare context from retrieved documents
            context = "\n\n".join([
                f"Source: {doc['title']}\nCategory: {doc.get('category', 'General')}\nContent: {doc['content']}"
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
            weighted_score += min(doc['score'], 1.0) * weight  # Cap individual scores at 1.0
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
        """Add new document to knowledge base."""
        try:
            # Add to knowledge base
            new_doc = {
                "title": title,
                "content": content,
                "category": category
            }
            
            self.documents.append(new_doc)
            
            print(f"✅ Added new document to knowledge base: {title}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding document to knowledge base: {e}")
            return False