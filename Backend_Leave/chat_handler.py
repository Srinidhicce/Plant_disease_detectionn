import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAaVTlsI8qELmDYbV8B7Y_MVP80TuhPvjs"  # replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat()

def get_chat_response(message):
    response = chat.send_message(message)
    return response.text
