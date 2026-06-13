# 🤖 Documents Assistant - Engine: Gemini 2.5 Flash

**Documents Assistant** is a powerful, multilingual AI-powered tool that allows users to chat with their PDF documents. Built with **Streamlit**, **LangChain**, and **Google Gemini**, it provides an intuitive interface for document analysis with a strong focus on user privacy.

---

## ✨ Key Features

*   **Chat with PDF:** Upload any PDF and ask questions about its content instantly.
*   **Multilingual Support:** Switch between **English**, **Vietnamese**, and **Finnish (Suomi)** seamlessly.
*   **Privacy First:** All documents are processed in-memory (RAM) and are automatically deleted when the browser is closed. No files are stored on our servers.
*   **Hybrid API Mode:** 
    *   **System Key:** Limited to 10 free questions (usage tracked via LocalStorage).
    *   **Personal Key:** Unlimited usage by providing your own Google Gemini API Key.
*   **Real-time Validation:** Instant API Key verification to ensure seamless performance.

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **LLM:** Google Gemini 2.5 Flash
- **Framework:** LangChain
- **Document Processing:** PDFPlumber
- **Embedding Model:** Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database:** ChromaDB (In-Memory)
- **Client-side Persistence:** Streamlit-Javascript (LocalStorage)

---

## 🚀 Quick Start

### 1. Prerequisites
Make sure you have Python 3.9 or higher installed.

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/documents-assistant-gemini.git](https://github.com/your-username/documents-assistant-gemini.git)
cd documents-assistant-gemini
```
### 3. Install Dependencies

Install the required Python packages using pip: `pip install -r requirements.txt`

### 4. Configuration

Create a .env file in the root directory and add your Google Gemini API Key: `GOOGLE_API_KEY=your_api_key_here   `

### 5. Run the Application

Start the Streamlit server locally:
`streamlit run app.py`
    

🔒 Privacy & Security
---------------------

*   **No Persistence:** Uploaded files are converted into vector embeddings in volatile RAM. Once the session is closed or the browser is refreshed, all data is wiped.
    
*   **Secure API Handling:** User-provided API keys are only used for the current session and are never logged, stored, or saved to any database.
    
*   **Client-side Usage Tracking:** Free usage counts (10 messages limit) are stored in the user's browser via **LocalStorage**, ensuring privacy and preventing unnecessary server-side tracking.
    

If you have any questions, feedback, or want to contribute, feel free to reach out or open an issue in this repository.
