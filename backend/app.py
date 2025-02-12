from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import ollama
import requests
from bs4 import BeautifulSoup
import gtts
import os
import PyPDF2
import re
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

# Extract text from a webpage URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None, f"Error fetching URL: {response.status_code}"
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text_content = " ".join([para.get_text() for para in paragraphs])
        return text_content, None
    except Exception as e:
        return None, f"Exception in URL processing: {str(e)}"

# Extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        return text, None
    except Exception as e:
        return None, f"Exception in PDF processing: {str(e)}"

# Function to remove AI's reasoning from podcast audio
def remove_thinking_process(response_text):
    return re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()

# Function to split long text into chunks
def split_text_into_chunks(text, chunk_size=5000, overlap=500):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

@app.route('/generate', methods=['POST'])
def generate():
    extracted_text = ""
    error_message = None

    data = request.get_json(silent=True) or {}
    url = data.get("url", "")
    show_thinking = data.get("show_thinking", True)
    language = data.get("language", "en")

    if url:
        extracted_text, error_message = extract_text_from_url(url)

    if "file" in request.files:
        pdf_file = request.files["file"]
        pdf_text, pdf_error = extract_text_from_pdf(pdf_file)
        extracted_text += pdf_text if pdf_text else ""
        if pdf_error:
            error_message = pdf_error

    if error_message:
        return jsonify({"error": error_message}), 400

    if not extracted_text.strip():
        return jsonify({"error": "No valid text extracted"}), 400

    try:
        text_chunks = split_text_into_chunks(extracted_text)
        final_response = ""
        final_podcast_text = ""

        for chunk in text_chunks:
            prompt = f"""
            Act as a podcast host and a guest discussing this research.
            Provide a structured discussion with back-and-forth dialogue.

            Text:
            {chunk}
            """

            response = ollama.chat(model='deepseek-r1:1.5b', messages=[{"role": "user", "content": prompt}])
            ai_response = response['message']['content']

            final_response += ai_response + "\n\n"
            final_podcast_text += remove_thinking_process(ai_response) + "\n\n"

        if language != "en":
            final_podcast_text = GoogleTranslator(source='auto', target=language).translate(final_podcast_text)
            final_response = GoogleTranslator(source='auto', target=language).translate(final_response)

        tts = gtts.gTTS(final_podcast_text, lang=language)
        tts.save("output.mp3")

        return jsonify({
            "response": final_response,
            "summary_only": final_podcast_text,
            "audio_url": "/get_audio"
        })
    except Exception as e:
        return jsonify({"error": f"AI processing failed: {str(e)}"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    history = data.get("history", [])  # Retrieve previous chat history

    messages = [{"role": "system", "content": "You are an AI assistant for research discussions."}]
    
    for role, message in history:
        messages.append({"role": "user" if role == "You" else "assistant", "content": message})
    
    messages.append({"role": "user", "content": user_message})

    chat_response = ollama.chat(model='deepseek-r1:1.5b', messages=messages)

    return jsonify({"response": chat_response['message']['content']})

@app.route('/get_audio', methods=['GET'])
def get_audio():
    return send_file("output.mp3", as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)