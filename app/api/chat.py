from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user
from app.services.rag_service import rag_service
from app.services.emergency_service import EmergencyService
from app.core.database import get_db
from datetime import datetime, timezone

router = APIRouter()
emergency = EmergencyService()

@router.post("/send")
async def send_message(
    body: dict,
    current_user: dict = Depends(get_current_user)
):
    db = get_db()
    user_message = body.get("message", "")
    user_id = current_user["user_id"]
    
    # Step 1: Emergency check
    emergency_result = emergency.check(user_message)
    if emergency_result["is_emergency"]:
        return {
            "reply": emergency_result["message"],
            "is_emergency": True
        }
    
    # Step 2: Chat history lo
    history = await db["messages"].find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(6).to_list(6)
    history.reverse()
    
    # Step 3: RAG + LLM
    reply = await rag_service.get_response(
        user_message=user_message,
        chat_history=history
    )
    
    # Step 4: Save karo
    await db["messages"].insert_many([
        {
            "user_id": user_id,
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "user_id": user_id,
            "role": "assistant",
            "content": reply,
            "timestamp": datetime.now(timezone.utc)
        }
    ])
    
    return {"reply": reply, "is_emergency": False}

@router.get("/history")
async def get_history(current_user: dict = Depends(get_current_user)):
    db = get_db()
    messages = await db["messages"].find(
        {"user_id": current_user["user_id"]}
    ).sort("timestamp", 1).to_list(50)
    
    return [
        {
            "role": msg["role"],
            "content": msg["content"],
            "timestamp": str(msg["timestamp"])
        }
        for msg in messages
    ]