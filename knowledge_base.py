import json
import os
from typing import List, Dict, Any

class KnowledgeBase:
    def __init__(self, data_file: str = "data/knowledge_base.json"):
        """Initialize knowledge base with data from JSON file."""
        self.data_file = data_file
        self.documents = []
        self._load_data()
    
    def _load_data(self):
        """Load knowledge base data from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.documents = data.get('documents', [])
            else:
                print(f"⚠️ Knowledge base file not found: {self.data_file}")
                self.documents = []
            
            print(f"✅ Loaded {len(self.documents)} documents from knowledge base")
            
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            self.documents = []
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Return all documents in the knowledge base."""
        return self.documents
    
    def get_documents_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Return documents filtered by category."""
        return [doc for doc in self.documents if doc.get('category') == category]
    
    def search_documents(self, keyword: str) -> List[Dict[str, Any]]:
        """Search documents by keyword in title or content."""
        keyword_lower = keyword.lower()
        results = []
        
        for doc in self.documents:
            if (keyword_lower in doc.get('title', '').lower() or 
                keyword_lower in doc.get('content', '').lower()):
                results.append(doc)
        
        return results
    
    def add_document(self, title: str, content: str, category: str = "General") -> bool:
        """Add a new document to the knowledge base."""
        try:
            new_doc = {
                "title": title,
                "content": content,
                "category": category
            }
            
            self.documents.append(new_doc)
            self._save_data()
            return True
            
        except Exception as e:
            print(f"❌ Error adding document: {e}")
            return False
    
    def _save_data(self):
        """Save knowledge base data to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = {
                "documents": self.documents,
                "last_updated": "2025-07-24"
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Knowledge base saved to {self.data_file}")
            
        except Exception as e:
            print(f"❌ Error saving knowledge base: {e}")
    
    def get_categories(self) -> List[str]:
        """Get all unique categories in the knowledge base."""
        categories = set()
        for doc in self.documents:
            categories.add(doc.get('category', 'General'))
        return sorted(list(categories))
    
    def get_document_count(self) -> int:
        """Get total number of documents."""
        return len(self.documents)
