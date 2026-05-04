from app.services.llm_service import llm_service
import os

class RAGService:
    def __init__(self):
        self.knowledge_base = []
        self._load_knowledge()
    
    def _load_knowledge(self):
        kb_path = "./Knowledge Database/"
        if not os.path.exists(kb_path):
            os.makedirs(kb_path)
            return
        
        for filename in os.listdir(kb_path):
            if filename.endswith(".txt"):
                with open(f"{kb_path}{filename}", "r", encoding="utf-8") as f:
                    self.knowledge_base.append(f.read())
    
    def _get_relevant_context(self, query: str) -> str:
        if not self.knowledge_base:
            return "No knowledge base available."
        
        query_words = query.lower().split()
        scored = []
        
        for doc in self.knowledge_base:
            score = sum(1 for word in query_words if word in doc.lower())
            scored.append((score, doc))
        
        scored.sort(reverse=True)
        top_docs = [doc for _, doc in scored[:2]]
        return "\n\n".join(top_docs)
    
    async def get_response(
        self,
        user_message: str,
        chat_history: list = []
    ) -> str:
        context = self._get_relevant_context(user_message)
        response = await llm_service.get_response(
            user_message=user_message,
            context=context,
            chat_history=chat_history
        )
        return response

rag_service = RAGService()