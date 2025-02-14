# **VedaVani - AI-Powered Discussions**

🚀 **VedaVani** revolutionizes the accessibility of scholarly content by transforming 📄 research papers and 🌐 web articles into **🧠 AI-generated 🎙️ discussions** and **🎧 podcasts**, enabling seamless consumption of complex information.

---
[vedavani_recorded.webm](https://github.com/user-attachments/assets/579fc80b-1fab-4d1d-b7fc-b879ce3d5f66)

## **📌✨ Features**

✅ **🤖 AI-Generated Discussions** – Converts textual input into **structured conversational narratives**.
✅ **🔗 URL & 📂 PDF Compatibility** – Supports both direct web links and uploaded document files.
✅ **🎧 Podcast Synthesis** – Generates **🗣️ AI-narrated** audio summaries with dynamic speaker interactions.
✅ **📥 Downloadable Audio** – Facilitates offline accessibility of synthesized discussions.

---

## **📥💻 Installation**

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/yourusername/VedaVani.git
cd VedaVani
```

### **2️⃣ Set Up a Virtual Environment**

```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**

```sh
pip install -r requirements.txt
              OR
pip install --upgrade pip setuptools wheel
pip install streamlit flask flask-cors ollama beautifulsoup4 gtts PyPDF2 deep-translator requests pyarrow
```

### **4️⃣ Run the Backend (Flask API)**

```sh
cd backend
python app.py
```

✅ **Flask API is accessible at:** `http://127.0.0.1:5001`

### **5️⃣ Run the Frontend (Streamlit Interface)**

```sh
cd frontend
streamlit run main.py
```

✅ **VedaVani UI is available at:** `http://localhost:8501`

---

## **📌📖 Usage Guide**

1️⃣ **Provide Input:** Paste a research URL or upload a PDF.
2️⃣ **Select Preferences:** Choose podcast and summarization options.
3️⃣ **Generate Content:** Click **🎬 "Generate Podcast"** to initiate the AI-driven discussion.
4️⃣ **Engage with the Output:** Listen to the synthesized podcast and download it for future reference.

---

## **📌📂 Project Structure**

```
VedaVani/
│── backend/       # Backend API (Flask)
│   ├── app.py     # API logic implementation
│   ├── requirements.txt  # Dependency management
│── frontend/      # UI Layer (Streamlit)
│   ├── main.py    # Frontend application logic
│── venv/         # Virtual Environment (excluded from version control)
│── README.md     # Documentation
│── .gitignore    # Excluded files
```

---

## **📌🛠️ Technology Stack**

- **🔥 Flask** – Backend API framework
- **🎨 Streamlit** – Interactive user interface development
- **🧠 DeepSeek AI (via Ollama)** – AI-powered dialogue generation
- **🌐 BeautifulSoup** – Web scraping for URL-based text extraction
- **📄 PyPDF2** – PDF content processing
- **🌍 GoogleTranslator API** – Multilingual translation support
- **🎙️ gTTS (Google Text-to-Speech)** – AI-enhanced podcast narration

---

## **📌💡 Contributing**

🛠️ **Contributions are welcomed!** Engage through **bug reports, feature suggestions, and pull requests.**

1. **🔀 Fork the repository**
2. **🌱 Create a feature branch:** `git checkout -b feature-enhancement`
3. **✅ Commit changes:** `git commit -m "✨ Implemented new feature"`
4. **🚀 Push to branch:** `git push origin feature-enhancement`
5. **🎉 Open a pull request!**

---

## **📌📜 License**

📜 **Licensed under MIT** – You are free to modify and distribute this project with proper attribution.

---

## **📌📩 Contact**

📧 For inquiries, contact [nihalgbailur@gmail.com](mailto:nihalgbailur@gmail.com)
🔗 Follow on **GitHub**: [@nihalgbailur](https://github.com/nihalgbailur)

---

## **📌🎯 Future Enhancements**

🔹 **🗣️ Advanced voice synthesis (ElevenLabs integration)**
🔹 **🎭 Multiple AI-driven speakers for enhanced podcast immersion**
🔹 **📚 High-fidelity summarization with Mistral/LLama3 models**

---

### **🚀 Star this repository if you find it useful!**

