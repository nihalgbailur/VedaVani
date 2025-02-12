import streamlit as st
import requests

st.set_page_config(page_title="VedaVani - AI Research Talk", layout="wide")

st.title("📜 VedaVani - AI-Generated Research Podcasts")
st.write("Enter a URL and/or upload a PDF, and AI will generate a conversational podcast.")

# Toggle for showing AI's thinking process
show_thinking = st.checkbox("Show AI Thinking", value=True)

# URL Input
input_url = st.text_input("Paste the URL here:")

# PDF Upload
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Language Selection for AI Summary
language_options = {"English": "en", "Kannada": "kn", "Hindi": "hi", "Telugu": "te"}
selected_language = st.selectbox("Select Summary Language", list(language_options.keys()))

if st.button("Generate Podcast"):
    if not input_url and not uploaded_file:
        st.warning("Please enter a URL and/or upload a PDF.")
    else:
        with st.spinner("Processing..."):
            try:
                # Prepare request payload
                payload = {
                    "url": input_url if input_url else None,
                    "show_thinking": show_thinking,  # Pass toggle value to backend
                    "language": language_options[selected_language],  # Pass selected language
                }

                # If a PDF file is uploaded, send it with the request
                if uploaded_file:
                    files = {"file": uploaded_file.getvalue()}  # Read file bytes
                    response = requests.post("http://127.0.0.1:5001/generate", files=files, data=payload)
                else:
                    headers = {"Content-Type": "application/json"}
                    response = requests.post("http://127.0.0.1:5001/generate", json=payload, headers=headers)

                # Handle response
                data = response.json()
                
                if "response" in data:
                    st.subheader("🗣️ AI-Generated Discussion:")
                    if show_thinking:
                        st.write(data["response"])  # Show full response including AI Thinking
                    else:
                        st.write(data["summary_only"])  # Show only the structured summary
                    
                    st.subheader("🎙️ Listen to the AI-Generated Podcast:")
                    st.audio("http://127.0.0.1:5001/get_audio")

                    st.download_button("Download Podcast", "http://127.0.0.1:5001/get_audio", file_name="VedaVani_Podcast.mp3")
                elif "error" in data:
                    st.error(f"Error: {data['error']}")
                else:
                    st.error("Unknown error occurred.")
            except requests.exceptions.ConnectionError:
                st.error("Error: Could not connect to the backend. Is Flask running?")

st.markdown("---")
st.caption("🚀 Powered by DeepSeek & Streamlit")