from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

class LLMService:
    
    async def get_response(
        self,
        user_message: str,
        context: str,
        chat_history: list = []
    ) -> str:
        
        messages = [
            {
                "role": "system",
                "content": f"""Tu SwasthyaBot hai — ek helpful AI health assistant.
Tu Hindi aur English dono mein baat karta hai.

HEALTH KNOWLEDGE:
{context}

RULES:
- Sirf health topics pe baat karo
- Koi bhi disease definitively diagnose mat karo
- Emergency mein 112 call karne kaho
- Har jawab ke end mein doctor se milne ki salah do"""
            }
        ]
        
        for msg in chat_history[-6:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        
        return response.choices[0].message.content

llm_service = LLMService()