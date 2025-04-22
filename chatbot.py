import os
from groq import Groq
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


class UserMessage(BaseModel):
    msg : str

@app.api_route("/ping", methods=["GET", "HEAD"])
async def ping():
    await asyncio.sleep(0.1)
    return {"message": "server is running"}



@app.post("/chat")
async def chat_with_doctor(ui: UserMessage):

    chat_hist= [{"role": "system", "content": "You are a strictly legal assistant chatbot, providing only legal advice and information. Your responses should cover all areas of law, including criminal and victim perspectives, ensuring you remain impartial and open-minded. If a user veers off-topic with irrelevant content, such as HTML code or jokes, politely redirect them back to the legal matters, maintaining professionalism at all times. Avoid engaging in non-legal discussions and always ensure that your tone is respectful, clear, and focused on delivering accurate legal guidance. Direct users to appropriate professionals when necessary."}]

    ui = ui.msg
    chat_hist.append({"role": "user", "content": ui})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_hist,
            temperature=0.2,
            max_tokens=512,
        )
        res = completion.choices[0].message.content
        chat_hist.append({"role": "assistant", "content": res})
        return {"response":res}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)