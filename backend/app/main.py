from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Conversation, Message
from .schemas import ChatRequest, ChatResponse
from .ai_service import generate_reply

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Customer Service Platform API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Message cannot be blank.")

    conversation = Conversation()
    db.add(conversation)
    db.flush()

    user_message = Message(
        conversation_id=conversation.id,
        sender="customer",
        content=message,
    )
    reply, mode = generate_reply(message)
    assistant_message = Message(
        conversation_id=conversation.id,
        sender="assistant",
        content=reply,
    )
    db.add_all([user_message, assistant_message])
    db.commit()
    db.refresh(conversation)

    return ChatResponse(
        conversation_id=conversation.id,
        reply=reply,
        mode=mode,
    )
