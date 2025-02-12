import streamlit as st
import requests

st.set_page_config(page_title="VedaVani - AI Research Chat & Podcast", layout="wide")

st.title("📜 VedaVani - AI Research Chat & Podcast")

input_url = st.text_input("📎 Enter Website URL (Optional)")
uploaded_file = st.file_uploader("📂 Upload Research Paper (PDF)", type=["pdf"])

show_thinking = st.checkbox("🤖 Show AI Thinking", value=True)

language_options = {"English": "en", "Kannada": "kn", "Hindi": "hi", "Telugu": "te"}
selected_language = st.selectbox("🌍 Select Summary Language", list(language_options.keys()))

if st.button("🎙️ Generate Podcast"):
    payload = {"url": input_url, "show_thinking": show_thinking, "language": language_options[selected_language]}
    
    response = requests.post("http://127.0.0.1:5001/generate", json=payload)
    data = response.json()

    if "response" in data:
        st.subheader("🗣️ AI-Generated Discussion:")
        st.write(data["response"] if show_thinking else data["summary_only"])

        st.subheader("🎧 Listen to the AI-Generated Podcast:")
        st.audio("http://127.0.0.1:5001/get_audio")
        st.download_button("⬇️ Download Podcast", "http://127.0.0.1:5001/get_audio", file_name="VedaVani_Podcast.mp3")

chat_input = st.text_input("💬 Chat with VedaVani AI")
if st.button("🤖 Ask AI"):
    chat_response = requests.post("http://127.0.0.1:5001/chat", json={"message": chat_input}).json()
    st.write(f"🤖 AI: {chat_response['response']}")

if st.button("🔄 Clear Chat"):
    requests.post("http://127.0.0.1:5001/chat", json={"message": "/clear"})
    st.rerun()