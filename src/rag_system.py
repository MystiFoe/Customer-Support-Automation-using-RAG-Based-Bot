import re
from typing import List, Dict, Any
from openai import OpenAI
from src.knowledge_base import KnowledgeBase
from src.logger import get_logger
from config.settings import config

logger = get_logger(__name__)


class RAGSystem:
    def __init__(self, knowledge_base_path: str):
        self.client = OpenAI(api_key=config.openai.api_key)
        self.knowledge_base = KnowledgeBase(knowledge_base_path)
        logger.info("RAG System initialized with %d documents", 
                   self.knowledge_base.get_document_count())
    
    def _retrieve_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        try:
            query_words = set(re.findall(r'\w+', query.lower()))
            scored_docs = []
            
            for doc in self.knowledge_base.get_all_documents():
                title_words = set(re.findall(r'\w+', doc.get('title', '').lower()))
                content_words = set(re.findall(r'\w+', doc.get('content', '').lower()))
                
                title_score = len(query_words.intersection(title_words)) * 3
                content_score = len(query_words.intersection(content_words)) * 1
                
                total_score = title_score + content_score
                
                if total_score > 0:
                    doc_copy = doc.copy()
                    doc_copy['score'] = total_score / max(len(query_words), 1)
                    scored_docs.append(doc_copy)
            
            scored_docs.sort(key=lambda x: x['score'], reverse=True)
            return scored_docs[:top_k]
            
        except Exception as e:
            logger.error("Error retrieving documents: %s", str(e))
            return []
    
    def _generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            context = "\n\n".join([
                f"Source: {doc['title']}\nContent: {doc['content']}"
                for doc in context_docs
            ])
            
            system_prompt = '''You are a professional customer support assistant. 
            Use the provided context to answer questions accurately and helpfully.
            
            Guidelines:
            - Provide clear, concise answers
            - Use information from the context when available
            - If context is insufficient, recommend contacting human support
            - Maintain a professional, helpful tone'''
            
            user_prompt = f'''Context:\n{context}\n\nQuestion: {query}\n\nPlease provide a helpful response based on the context above.'''
            
            response = self.client.chat.completions.create(
                model=config.openai.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=config.openai.max_tokens,
                temperature=config.openai.temperature
            )
            
            answer = response.choices[0].message.content
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
            logger.error("Error generating response: %s", str(e))
            return {
                "answer": "I apologize, but I'm experiencing technical difficulties. Please contact our support team for assistance.",
                "confidence": 0.0,
                "sources": []
            }
    
    def _calculate_confidence(self, context_docs: List[Dict[str, Any]]) -> float:
        if not context_docs:
            return 0.0
        
        weights = [1.0, 0.7, 0.5]
        weighted_score = 0.0
        total_weight = 0.0
        
        for i, doc in enumerate(context_docs[:3]):
            weight = weights[i] if i < len(weights) else 0.3
            weighted_score += min(doc['score'], 1.0) * weight
            total_weight += weight
        
        confidence = (weighted_score / total_weight) if total_weight > 0 else 0.0
        return min(1.0, max(0.0, confidence))
    
    def get_response(self, query: str) -> Dict[str, Any]:
        try:
            relevant_docs = self._retrieve_documents(query, top_k=3)
            response_data = self._generate_response(query, relevant_docs)
            return response_data
        except Exception as e:
            logger.error("Error in RAG system: %s", str(e))
            return {
                "answer": "I'm currently experiencing technical issues. Please try again later or contact human support.",
                "confidence": 0.0,
                "sources": []
            }