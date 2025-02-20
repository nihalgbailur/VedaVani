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

    # Update UI controls with columns and expanders
    col1, col2 = st.columns(2)
    
    with col1:
        language_options = {"English": "en", "Kannada": "kn", "Hindi": "hi", "Telugu": "te"}
        selected_language = st.selectbox("🌍 Select Summary Language", list(language_options.keys()))
    
    with col2:
        # Replace checkboxes with expanders
        with st.expander("⚙️ Advanced Options"):
            show_thinking = st.toggle("🤔 Show AI Thinking Process", value=False)
            show_conversation = st.toggle("🗨️ Show Full Conversation", value=True)

    if st.button("🎙️ Generate Podcast", type="primary", use_container_width=True):
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

                    # Improved thinking display
                    if show_thinking and "thinking_part" in data:
                        with st.expander("🧠 View AI Thinking Process", expanded=False):
                            thinking_lines = data["thinking_part"].split("\n")
                            for line in thinking_lines:
                                if line.strip():
                                    st.info(line)

                    # Improved conversation display
                    if show_conversation and "response" in data:
                        with st.expander("🗨️ View Full Conversation", expanded=True):
                            conversation_lines = data["response"].split("\n")
                            for line in conversation_lines:
                                if line.strip():
                                    if line.startswith("Host:"):
                                        st.markdown(f"""
                                        <div style='background-color: #e6f3ff; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                                            💙 <b>Host:</b> {line.replace('Host:', '')}
                                        </div>
                                        """, unsafe_allow_html=True)
                                    elif line.startswith("Guest:"):
                                        st.markdown(f"""
                                        <div style='background-color: #f0fff0; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                                            💚 <b>Guest:</b> {line.replace('Guest:', '')}
                                        </div>
                                        """, unsafe_allow_html=True)

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

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "thinking" not in st.session_state:
        st.session_state.thinking = False

    # Custom CSS with loading animation
    st.markdown("""
        <style>
        .chat-message-user {
            background-color: #2e3136;
            color: #ffffff;
            padding: 15px;
            border-radius: 15px;
            margin: 5px 0;
            text-align: right;
            border: 1px solid #404040;
        }
        .chat-message-ai {
            background-color: #1e1e1e;
            color: #ffffff;
            padding: 15px;
            border-radius: 15px;
            margin: 5px 0;
            border: 1px solid #404040;
        }
        .thinking-animation {
            color: #0078D4;
            padding: 10px;
            border-radius: 15px;
            margin: 5px 0;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        .stTextInput input {
            background-color: #2e3136;
            color: white;
            border: 1px solid #404040;
        }
        .stTextInput input:focus {
            border-color: #0078D4;
        }
        </style>
    """, unsafe_allow_html=True)

    # Optimized message sending function
    def send_message():
        if st.session_state.user_input.strip():
            user_message = st.session_state.user_input
            st.session_state.thinking = True
            st.session_state.chat_history.append(("You", user_message))
            st.session_state.user_input = ""
            st.rerun()  # Rerun here to show the user message immediately
            
            try:
                chat_payload = {
                    "message": user_message,
                    "history": st.session_state.chat_history[-5:]  # Only send last 5 messages for context
                }
                chat_response = requests.post(
                    "http://127.0.0.1:5001/chat",
                    json=chat_payload,
                    timeout=10  # Add timeout
                ).json()
                
                if "response" in chat_response:
                    st.session_state.chat_history.append(("VedaVani AI", chat_response["response"]))
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                st.session_state.thinking = False
                st.rerun()  # Rerun after getting the response

    # Display chat messages with thinking indicator
    chat_container = st.container()
    with chat_container:
        for role, message in st.session_state.chat_history:
            if role == "You":
                st.markdown(f"""
                <div class="chat-message-user">
                    🧑 <b>You:</b> {message}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message-ai">
                    🤖 <b>VedaVani AI:</b> {message}
                </div>
                """, unsafe_allow_html=True)
        
        # Show thinking animation
        if st.session_state.thinking:
            st.markdown("""
            <div class="thinking-animation">
                🤖 VedaVani AI is thinking...
            </div>
            """, unsafe_allow_html=True)

    # Optimized input area
    st.markdown("---")
    input_container = st.container()
    with input_container:
        col1, col2, col3 = st.columns([6, 1, 1])
        
        with col1:
            # Add on_change handler for Enter key
            st.text_input(
                "💭 Ask VedaVani AI:",
                key="user_input",
                value=st.session_state.user_input,
                placeholder="Type your message here...",
                disabled=st.session_state.thinking,
                on_change=send_message if st.session_state.user_input and not st.session_state.thinking else None
            )
        
        with col2:
            # Simplify button logic
            st.button(
                "💬 Send",
                on_click=send_message,
                type="primary",
                use_container_width=True,
                disabled=st.session_state.thinking
            )
        
        with col3:
            if st.button("🔄 Clear", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.user_input = ""
                st.session_state.thinking = False
                st.rerun()

st.markdown("---")
st.caption("🚀 Powered by DeepSeek & Streamlit")