from sanic import Sanic
from sanic.response import HTTPResponse
from sanic.request import Request
from sanic import response

import re
import json
import httpx
import os
import openai

TOKEN = str(os.getenv("TELEGRAM_BOT_TOKEN"))
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

client = httpx.AsyncClient()

app = Sanic(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = []

class ChatGPT:
    def __init__(self):
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")

    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        
        response = openai.Completion.create(
            engine=self.model,
            prompt=f"{conversation[-1]['role']}: {conversation[-1]['content']}\nAI:",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        
        message = response.choices[0].text.strip()
        conversation.append({"role": "assistant", "content": message})
        
        print("AI回答內容：")        
        print(message)

        return message

chatgpt = ChatGPT()

@app.route("/")
async def handle_request(request: Request) -> HTTPResponse:
    return response.text("Hello!")
'''
@app.post("/callback")
async def callback(request: Request) -> HTTPResponse:
    data = await request.json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]
    ai_reply_response = chatgpt.get_response(text)
    await client.get(f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={ai_reply_response}")
    return response.text("OK")
'''
@app.post("/callback")
async def callback(request: Request) -> HTTPResponse:
    req_data = await request.json()
    chat_id = req_data['message']['chat']['id']
    text = req_data['message']['text']
    ai_reply_response = chatgpt.get_response(text)  
    await client.get(f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={ai_reply_response}")
    return response.text("OK")

