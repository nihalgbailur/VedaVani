import streamlit as st
import requests

st.set_page_config(page_title="VedaVani - AI Research Chat & Podcast", layout="wide")

st.title("📜 VedaVani - AI Research Chat & Podcast")

# Upload PDF or Enter URL
st.subheader("📥 Upload Research Paper or Enter URL")
input_url = st.text_input("🔗 Paste Website URL (Optional)")
uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])

# Toggle for showing AI's thinking process
show_thinking = st.checkbox("🤔 Show AI Thinking", value=True)

# Language selection
language_options = {"English": "en", "Kannada": "kn", "Hindi": "hi", "Telugu": "te"}
selected_language = st.selectbox("🌍 Select Summary Language", list(language_options.keys()))

# Generate Podcast Button
if st.button("🎙️ Generate Podcast"):
    with st.spinner("Processing... 🎧"):
        payload = {
            "url": input_url,
            "show_thinking": show_thinking,
            "language": language_options[selected_language]
        }
        
        # Handle both URL and PDF file uploads
        if uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post("http://127.0.0.1:5001/generate", files=files, data=payload)
        else:
            response = requests.post("http://127.0.0.1:5001/generate", json=payload)

        # Process Response
        try:
            data = response.json()
            if "response" in data:
                st.subheader("🗣️ AI-Generated Discussion:")
                st.write(data["response"] if show_thinking else data["summary_only"])

                st.subheader("🎧 Listen to AI-Generated Podcast:")
                st.audio("http://127.0.0.1:5001/get_audio")
                st.download_button("⬇️ Download Podcast", "http://127.0.0.1:5001/get_audio", file_name="VedaVani_Podcast.mp3")
            elif "error" in data:
                st.error(f"⚠️ Error: {data['error']}")
            else:
                st.error("⚠️ Unknown error occurred.")
        except requests.exceptions.JSONDecodeError:
            st.error("⚠️ Server Error: Received non-JSON response.")
            st.write(response.text)  # Debugging

# Chat Section
st.subheader("💬 Chat with VedaVani AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("📝 Ask any question:")

if st.button("🤖 Ask AI"):
    if user_input:
        chat_payload = {
            "message": user_input,
            "history": st.session_state.chat_history  # Send past chat messages for memory
        }
        chat_response = requests.post("http://127.0.0.1:5001/chat", json=chat_payload).json()
        
        if "response" in chat_response:
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("VedaVani AI", chat_response["response"]))

# Display Chat History
for role, message in st.session_state.chat_history:
    st.write(f"**{role}:** {message}")

# Clear Chat Button
if st.button("🔄 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

st.markdown("---")
st.caption("🚀 Powered by DeepSeek & Streamlit")
