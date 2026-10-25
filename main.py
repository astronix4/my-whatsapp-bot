import asyncio
from wppconnect import WppConnect
import google.generativeai as genai

GEMINI_API_KEY = "AQ.Ab8RN6KZPKkbLDx9PPZ0oP9KhPUxqd6_gFmd4YcqXJtgixiEqw"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def on_message(client, message):
    if message.get('type') == 'chat' and not message.get('isGroup'):
        sender = message.get('from')
        incoming_text = message.get('body')
        try:
            prompt = f"You are a helpful assistant. Reply to this WhatsApp message shortly: {incoming_text}"
            response = model.generate_content(prompt)
            await client.send_text(sender, response.text)
        except Exception as e:
            print(f"Error: {e}")

async def main():
    client = WppConnect(session='ai_autoresponder')
    client.on_message(on_message)
    await client.start()

if __name__ == '__main__':
    asyncio.run(main())
