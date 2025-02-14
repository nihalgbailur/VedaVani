import streamlit as st
import requests

st.set_page_config(page_title="VedaVani - AI Research Chat & Podcast", layout="wide")
st.title("📜 VedaVani - AI Research Chat & Podcast")

# 📌 Tabs for Podcast and Chat
tab1, tab2 = st.tabs(["🎙️ Podcast Generator", "💬 Chat with VedaVani"])

with tab1:
    st.subheader("📥 Upload Research Paper or Enter URL")
    input_url = st.text_input("🔗 Paste Website URL (Optional)")
    uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])

    # ✅ New Checkboxes
    show_thinking = st.checkbox("🤔 Show AI Thinking", value=False)
    show_conversation = st.checkbox("🗨️ Show Full Conversation", value=True)

    language_options = {"English": "en", "Kannada": "kn", "Hindi": "hi", "Telugu": "te"}
    selected_language = st.selectbox("🌍 Select Summary Language", list(language_options.keys()))

    if st.button("🎙️ Generate Podcast"):
        with st.spinner("Processing Podcast... 🎧"):
            payload = {
                "url": input_url,
                "show_thinking": show_thinking,
                "show_conversation": show_conversation,  # Pass to backend
                "language": language_options[selected_language]
            }

            if uploaded_file:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post("http://127.0.0.1:5001/generate", files=files, data=payload)
            else:
                response = requests.post("http://127.0.0.1:5001/generate", json=payload)

            try:
                data = response.json()
                if "response" in data:
                    st.success("✅ Podcast Generated Successfully!")

                    # ✅ Show AI Thinking if checked
                    if show_thinking and "thinking_part" in data:
                        st.subheader("🧠 AI Thinking Process")
                        st.text_area("AI Thought Process:", value=data["thinking_part"], height=150)
                    

                    # ✅ Show Conversation if checkbox is enabled
                    if show_conversation and "response" in data:
                        st.subheader("🗨️ AI-Generated Host/Guest Conversation:")
                        conversation_lines = data["response"].split("\n")
                        for line in conversation_lines:
                            if line.startswith("Host:"):
                                st.markdown(f"💙 **Host:** {line.replace('Host:', '')}")
                            elif line.startswith("Guest:"):
                                 st.markdown(f"💚 **Guest:** {line.replace('Guest:', '')}")                            

                    # 🎧 Podcast Player
                    st.subheader("🎧 Listen to Podcast:")
                    st.audio("http://127.0.0.1:5001/get_audio")
                    st.download_button(
                        label="⬇️ Download Podcast",
                        data=requests.get("http://127.0.0.1:5001/get_audio").content,
                        file_name="VedaVani_Podcast.mp3",
                        mime="audio/mp3"
                    )
                else:
                    st.error(data.get("error", "⚠️ Podcast generation failed."))
            except Exception as e:
                st.error(f"Server Error: {e}")

with tab2:
    st.subheader("💬 Chat with VedaVani AI")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("📝 Ask VedaVani AI:")

    if st.button("🤖 Chat"):
        if user_input:
            chat_payload = {
                "message": user_input,
                "history": st.session_state.chat_history
            }
            chat_response = requests.post("http://127.0.0.1:5001/chat", json=chat_payload).json()
            if "response" in chat_response:
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("VedaVani AI", chat_response["response"]))

    for role, message in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"🧑 **You:** {message}")
        else:
            st.markdown(f"🤖 **VedaVani AI:** {message}")

    if st.button("🔄 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("---")
st.caption("🚀 Powered by DeepSeek & Streamlit")