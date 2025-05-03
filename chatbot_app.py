import json
import asyncio
import os
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Initialize OpenAI client for GitHub Models
client = AsyncOpenAI(
    base_url="https://models.github.ai/inference",
    api_key=GITHUB_TOKEN,
)

# Simulated intent categories
intents = ["greeting", "order_status", "return_request", "technical_issue", "unknown"]

# Feedback storage (in-memory for demo, use database in production)
feedback_log = []

# FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for feedback
class Feedback(BaseModel):
    user_input: str
    response: str
    rating: int  # 1-5
    timestamp: str = datetime.now().isoformat()

# System prompt for the model
SYSTEM_PROMPT = """
You are a customer service chatbot designed to provide instant, accurate, and context-aware responses. Your goals are to:
1. Automate common customer queries (e.g., greetings, order status, returns, technical issues).
2. Provide clear, friendly, and professional responses.
3. Identify when an issue is complex (e.g., urgent, legal, complaints, or unclear queries) and suggest escalation to a human agent.
4. If the query matches a known intent (greeting, order_status, return_request, technical_issue), respond appropriately. For unknown intents, ask for clarification.

Classify the user's input into one of these intents: greeting, order_status, return_request, technical_issue, or unknown.
Respond with a JSON object containing:
- "response": The reply to the user.
- "intent": The detected intent.
- "escalation": Boolean indicating if escalation is needed (true for complex issues).

Example:
User: "Where is my order?"
Response: {
  "response": "Please provide your order number, and I'll check the status for you.",
  "intent": "order_status",
  "escalation": false
}

Always return a valid JSON object with 'response', 'intent', and 'escalation' fields.
"""

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            user_input = json.loads(data)["message"]
            result = await process_input(user_input)
            
            # Send response
            await websocket.send_json({
                "message": result["response"],
                "intent": result["intent"],
                "timestamp": datetime.now().isoformat()
            })
            
            # Handle escalation
            if result["escalation"]:
                await websocket.send_json({
                    "message": "This issue seems complex. Connecting you to a human agent...",
                    "escalation": True
                })
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

async def process_input(user_input: str) -> Dict:
    """Process user input using GitHub Models API."""
    try:
        completion = await client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            response_format={"type": "json_object"}
        )
        result = json.loads(completion.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Error processing input: {e}")
        return {
            "response": "Sorry, I'm having trouble understanding. Could you clarify?",
            "intent": "unknown",
            "escalation": True
        }

# Endpoint to receive feedback
@app.post("/feedback")
async def receive_feedback(feedback: Feedback):
    feedback_log.append(feedback.dict())
    retrain_model()
    return {"status": "Feedback received"}

def retrain_model():
    """Simulate retraining model with feedback (placeholder)."""
    # In production, use feedback_log to fine-tune or update prompt
    pass

# Simulate continuous learning
async def continuous_learning():
    while True:
        if feedback_log:
            retrain_model()
        await asyncio.sleep(3600)  # Run hourly

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(continuous_learning())