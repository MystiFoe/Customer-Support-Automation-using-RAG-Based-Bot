import json
import os
from typing import List, Dict, Any, Optional
from src.logger import get_logger

logger = get_logger(__name__)


class KnowledgeBase:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.documents: List[Dict[str, Any]] = []
        self._load_data()
    
    def _load_data(self) -> None:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.documents = data.get('documents', [])
                logger.info("Loaded %d documents from knowledge base", len(self.documents))
            else:
                logger.warning("Knowledge base file not found: %s", self.data_file)
                self.documents = []
        except Exception as e:
            logger.error("Error loading knowledge base: %s", str(e))
            self.documents = []
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        return self.documents
    
    def search_documents(self, keyword: str) -> List[Dict[str, Any]]:
        keyword_lower = keyword.lower()
        results = []
        
        for doc in self.documents:
            title = doc.get('title', '').lower()
            content = doc.get('content', '').lower()
            
            if keyword_lower in title or keyword_lower in content:
                results.append(doc)
        
        return results
    
    def get_document_count(self) -> int:
        return len(self.documents)