import os
from pathlib import Path
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from utils import create_search_engine
from prompt import PROMPT
from streamlit_javascript import st_javascript


LANGUAGES = {
    "Tiếng Việt": {
        "title": "🤖 Trợ lý tài liệu - Gemini 2.5 Flash",
        "how_it_works": "🔒 **Bảo mật:** Tài liệu của bạn được xử lý tạm thời trong bộ nhớ và sẽ tự động xóa khi bạn đóng trình duyệt. Chúng tôi không lưu trữ file của bạn trên máy chủ.",
        "api_config": "⚙️ Cấu hình API",
        "use_custom_key": "Sử dụng API Key cá nhân",
        "key_help": "Bật để dùng key của bạn (không giới hạn). Tắt để dùng key hệ thống (giới hạn 10 câu).",
        "input_key": "Nhập Key của bạn",
        "valid_key": "✅ API Key hợp lệ!",
        "invalid_key": "❌ API Key không đúng. Vui lòng kiểm tra lại.",
        "info_key": "ℹ️ Vui lòng nhập Key cá nhân.",
        "upload_header": "📤 Tài liệu",
        "processing": "Đang xử lý...",
        "done": "✅ Xong!",
        "rem_usage": "💎 Lượt dùng còn lại",
        "key_error_chat": "⚠️ API Key không hợp lệ. Vui lòng nhập đúng Key để tiếp tục.",
        "limit_error": "❌ Bạn đã hết lượt dùng thử.",
        "chat_input": "Hỏi về tài liệu...",
        "welcome": "👈 Hãy tải file PDF lên để bắt đầu.",
        "validate_spinner": "Đang xác thực Key...",
        "upload_label": "Tải file PDF lên tại đây",
        "upload_help": "Kéo thả file vào đây hoặc bấm nút bên dưới. Tối đa 200MB.",
    },
    "English": {
        "title": "🤖 Documents Assistant - Gemini 2.5 Flash",
        "how_it_works": "🔒 **Privacy:** Your documents are processed in-memory and deleted when you close the browser. We do not store your files on our servers.",
        "api_config": "⚙️ API Configuration",
        "use_custom_key": "Use Personal API Key",
        "key_help": "Enable to use your own key (unlimited). Disable to use system key (10 questions limit).",
        "input_key": "Enter your Key",
        "valid_key": "✅ Valid API Key!",
        "invalid_key": "❌ Invalid API Key. Please check again.",
        "info_key": "ℹ️ Please enter your personal key.",
        "upload_header": "📤 Documents",
        "processing": "Processing...",
        "done": "✅ Done!",
        "rem_usage": "💎 Remaining uses",
        "key_error_chat": "⚠️ Invalid API Key. Please enter a valid key to continue.",
        "limit_error": "❌ You have reached the free trial limit.",
        "chat_input": "Ask about the document...",
        "welcome": "👈 Please upload a PDF file to start.",
        "validate_spinner": "Validating Key...",
        "upload_label": "Upload your PDF file here",
        "upload_help": "Drag and drop file here or click the button below. Max 200MB.",

    },
    "Suomi": {
        "title": "🤖 Dokumenttiavustaja - Gemini 2.5 Flash",
        "how_it_works": "🔒 **Tietosuoja:** Asiakirjasi käsitellään väliaikaisesti muistissa ja poistetaan, kun suljet selaimen. Emme tallenna tiedostojasi palvelimillemme.",
        "api_config": "⚙️ API-asetukset",
        "use_custom_key": "Käytä omaa API-avainta",
        "key_help": "Ota käyttöön käyttääksesi omaa avaintasi (rajoittamaton). Poista käytöstä käyttääksesi järjestelmäavainta (rajoitus 10 kysymystä).",
        "input_key": "Syötä avaimesi",
        "valid_key": "✅ API-avain on kelvollinen!",
        "invalid_key": "❌ Virheellinen API-avain. Tarkista uudelleen.",
        "info_key": "ℹ️ Syötä henkilökohtainen avaimesi.",
        "upload_header": "📤 Asiakirjat",
        "processing": "Käsitellään...",
        "done": "✅ Valmis!",
        "rem_usage": "💎 Kertoja jäljellä",
        "key_error_chat": "⚠️ Virheellinen API-avain. Syötä oikea avain jatkaaksesi.",
        "limit_error": "❌ Ilmaiset kokeilukerrat ovat täynnä.",
        "chat_input": "Kysy asiakirjasta...",
        "welcome": "👈 Lataa PDF-tiedosto aloittaaksesi.",
        "validate_spinner": "Vahvistetaan avainta...",
        "upload_label": "Lataa PDF-tiedosto tästä",
        "upload_help": "Vedä ja pudota tiedosto tähän tai klikkaa alla olevaa painiketta. Enintään 200MB.",
    }
}

# --- limit uses api
MAX_MESSAGES_FREE = 10 
current_dir = Path(__file__).parent.absolute()
env_file = current_dir / ".env"
if not env_file.exists(): env_file = current_dir.parent / ".env"
load_dotenv(dotenv_path=env_file)

def is_api_key_valid(api_key):
    if not api_key or len(api_key) < 30 or not api_key.startswith("AIza"):
        return False
    try:
        genai.configure(api_key=api_key)
        genai.get_model('models/gemini-2.5-flash')
        return True
    except Exception:
        return False

def get_system_api_key():
    try:
        if "GOOGLE_API_KEY" in st.secrets: return st.secrets["GOOGLE_API_KEY"]
    except: pass
    return os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Gemini PDF Assistant", page_icon="🤖", layout="wide")

# selected language
if "lang" not in st.session_state: st.session_state.lang = "Tiếng Việt"
with st.sidebar:
    st.session_state.lang = st.selectbox("🌐 Language / Kieli", options=list(LANGUAGES.keys()))
    t = LANGUAGES[st.session_state.lang] 

# count session usage
if "usage_count" not in st.session_state: st.session_state.usage_count = 0
js_get_usage = "localStorage.getItem('pdf_assistant_usage');"
stored_usage = st_javascript(js_get_usage)

if stored_usage is not None and str(stored_usage).isdigit():
    val = int(stored_usage)
    if val > st.session_state.usage_count:
        st.session_state.usage_count = val

if "messages" not in st.session_state: st.session_state.messages = []
if "chain" not in st.session_state: st.session_state.chain = None
if "processed_file" not in st.session_state: st.session_state.processed_file = None

def create_qa_chain(vector_store, api_key):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    chain = (
        {"context": (lambda x: x["question"]) | retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])),
         "question": lambda x: x["question"],
         "chat_history": lambda x: x["chat_history"]}
        | PROMPT | llm | StrOutputParser()
    )
    return chain, retriever

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.header(t["api_config"])
    use_custom_key = st.checkbox(t["use_custom_key"], value=False, help=t["key_help"])
    
    user_key = ""
    is_user_key_ok = False
    
    if use_custom_key:
        user_key = st.text_input(t["input_key"], type="password", key="user_api_key_input")
        if user_key:
            with st.spinner(t["validate_spinner"]):
                if is_api_key_valid(user_key):
                    st.success(t["valid_key"])
                    is_user_key_ok = True
                else:
                    st.error(t["invalid_key"])
        else:
            st.info(t["info_key"])
    
    system_key = get_system_api_key()
    
    if use_custom_key:
        final_api_key = user_key
        can_upload = is_user_key_ok 
        is_limited_mode = False
    else:
        final_api_key = system_key
        can_upload = bool(system_key)
        is_limited_mode = True

    st.divider()
    st.header(t["upload_header"])
    

    uploaded_file = st.file_uploader(
        label=t["upload_label"], 
        type=["pdf"], 
        disabled=not can_upload,
        help=t["upload_help"]
    )
    
    if uploaded_file and can_upload:
        if st.session_state.processed_file != uploaded_file.name:
            with st.status(t["processing"]) as status:
                try:
                
                    st.session_state.messages = []      
                    st.session_state.chain = None      
                    st.session_state.retriever = None  
                
                    vector_store, _ = create_search_engine(uploaded_file.getvalue())
            
                    st.session_state.chain, st.session_state.retriever = create_qa_chain(vector_store, final_api_key)
                    st.session_state.processed_file = uploaded_file.name
                    
                    status.update(label=t["done"], state="complete")
                    st.rerun() 
                except Exception as e: 
                    st.error(f"Error: {e}")

    if is_limited_mode and system_key:
        rem = MAX_MESSAGES_FREE - st.session_state.usage_count
        st.info(f"{t['rem_usage']}: {max(0, rem)}/{MAX_MESSAGES_FREE}")

# --- MAIN INTERFACE ---
st.title(t["title"])
st.caption(t["how_it_works"]) 
st.divider()

if st.session_state.chain:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    current_key_valid = is_user_key_ok if use_custom_key else bool(system_key)
    can_ask = not (is_limited_mode and st.session_state.usage_count >= MAX_MESSAGES_FREE)

    if not current_key_valid:
        st.error(t["key_error_chat"])
    elif not can_ask:
        st.error(f"{t['limit_error']} ({MAX_MESSAGES_FREE}/{MAX_MESSAGES_FREE})")
    else:
        if prompt := st.chat_input(t["chat_input"]):
            if is_limited_mode:
                st.session_state.usage_count += 1
                st_javascript(f"localStorage.setItem('pdf_assistant_usage', '{st.session_state.usage_count}');")

            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    history = [HumanMessage(content=m["content"]) if m["role"]=="user" 
                               else AIMessage(content=m["content"]) for m in st.session_state.messages[:-1]]
                    res = st.session_state.chain.invoke({"question": prompt, "chat_history": history})
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info(t["welcome"])