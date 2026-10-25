import os
import asyncio
from WPP_Whatsapp import Create
import google.generativeai as genai
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def on_message(message):
    if message.get('type') == 'chat' and not message.get('isGroupMsg'):
        sender = message.get('from')
        incoming_text = message.get('body')
        
        if incoming_text:
            try:
                prompt = f"You are a helpful assistant. Reply to this WhatsApp message shortly: {incoming_text}"
                response = model.generate_content(prompt)
                client.sendText(sender, response.text)
                print(f"Replied to {sender}")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    print("Starting WhatsApp Bot...")
    creator = Create(session='ai_autoresponder')
    client = creator.start()
    client.on_message(on_message)
    client.start()
    
