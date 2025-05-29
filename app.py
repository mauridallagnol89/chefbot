from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)
conversations = {}

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    phone_number = request.values.get("From", "").strip()
    
    if not incoming_msg:
        return "Mensagem vazia", 400

    if phone_number not in conversations:
        conversations[phone_number] = [system_prompt]
    
    conversations[phone_number].append(f"Usuário: {incoming_msg}")

    try:
        response = model.generate_content(conversations[phone_number])
        resposta = response.text
        conversations[phone_number].append(f"ChefBot: {resposta}")
    except Exception as e:
        resposta = "Desculpe, houve um erro ao processar sua mensagem."
        print("Erro:", e)

    twilio_response = MessagingResponse()
    twilio_response.message(resposta)
    return str(twilio_response)
