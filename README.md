# 🤖 Documents Assistant - Engine: Gemini 2.5 Flash

**Documents Assistant** is a powerful, multilingual AI-powered tool that allows users to chat with their PDF documents. Built with **Streamlit**, **LangChain**, and **Google Gemini**, it provides an intuitive interface for document analysis with a strong focus on user privacy.

---

## ✨ Key Features

*   **Chat with PDF:** Upload any PDF and ask questions about its content instantly.
*   **Multilingual Support:** Switch between **English**, **Vietnamese (Tiếng Việt)**, and **Finnish (Suomi)** seamlessly.
*   **Privacy First:** All documents are processed in-memory (RAM) and are automatically deleted when the browser is closed. No files are stored on our servers.
*   **Hybrid API Mode:** 
    *   **System Key:** Limited to 10 free questions (usage tracked via LocalStorage).
    *   **Personal Key:** Unlimited usage by providing your own Google Gemini API Key.
*   **Real-time Validation:** Instant API Key verification to ensure seamless performance.

---

## 🛠️ Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/)
*   **LLM Engine:** [Google Gemini 1.5/2.5 Flash](https://ai.google.dev/)
*   **Framework:** [LangChain](https://www.langchain.com/)
*   **Vector Store:** [FAISS](https://github.com/facebookresearch/faiss)
*   **PDF Processing:** [PyPDF](https://pypdf.readthedocs.io/)
*   **Client-side Sync:** [Streamlit-Javascript](https://github.com/noahshinn/streamlit-javascript)

---

## 🚀 Quick Start

### 1. Prerequisites
Make sure you have Python 3.9 or higher installed.

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/documents-assistant.git](https://github.com/your-username/documents-assistant.git)
cd documents-assistant

### 3\. Install Dependencies

Install the required Python packages using pip:

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

### 4\. Configuration

Create a .env file in the root directory and add your Google Gemini API Key:

Đoạn mã

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   GOOGLE_API_KEY=your_api_key_here   `

### 5\. Run the Application

Start the Streamlit server locally:

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   streamlit run app.py   `

📦 Deployment Guide
-------------------

### Deploying to Streamlit Cloud

1.  **Push your code** to a GitHub repository.
    
2.  Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
    
3.  Select the repository, branch, and the main file (app.py).
    
4.  **Important (Secrets Settings):**
    
    *   Before clicking **Deploy**, go to **Advanced Settings** > **Secrets**.
        
    *   Ini, TOMLGOOGLE\_API\_KEY = "your\_system\_api\_key\_here"
        
5.  Click **Deploy**.
    

🔒 Privacy & Security
---------------------

*   **No Persistence:** Uploaded files are converted into vector embeddings in volatile RAM. Once the session is closed or the browser is refreshed, all data is wiped.
    
*   **Secure API Handling:** User-provided API keys are only used for the current session and are never logged, stored, or saved to any database.
    
*   **Client-side Usage Tracking:** Free usage counts (10 messages limit) are stored in the user's browser via **LocalStorage**, ensuring privacy and preventing unnecessary server-side tracking.
    

📜 License
----------

Distributed under the **MIT License**. See LICENSE for more information.

🤝 Contact
----------

If you have any questions, feedback, or want to contribute, feel free to reach out or open an issue in this repository.