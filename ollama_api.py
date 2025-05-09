from fastapi import FastAPI, Body
from pydantic import BaseModel
from ollama import Client

app=FastAPI()
client=Client(
    host='http://localhost:11434'  # Updated to match the correct port
)
client.pull('gemma3:1b')

class ChatMessage(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ollama API!"}

@app.post("/chat", description="Chat Message")
def chat(message: ChatMessage):
    response = client.chat(model="gemma3:1b", messages=[
        {"role": "user", "content": message.content}
    ])

    return response['message']['content']