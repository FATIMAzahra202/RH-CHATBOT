from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
import streamlit as st
import os
import pandas as pd
import base64
import fitz
import tempfile
import re
from datetime import datetime
from ai_gemini import ask_gemini

load_dotenv()

st.set_page_config(page_title="Chat RH SEGULA", layout="centered")

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_faq_from_excel(path="questions_reponses_rh_segula.xlsx"):
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = df.columns.str.strip()
    questions = df.iloc[:, 3].astype(str).tolist()
    reponses = df.iloc[:, 4].fillna("").astype(str).tolist()
    return dict(zip(questions, reponses))

faq_data = load_faq_from_excel()
faq_questions = list(faq_data.keys())
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower().strip())

def extract_file_content(file):
    ext = file.name.split(".")[-1].lower()
    if ext == "txt":
        return file.read().decode("utf-8")
    elif ext == "pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp.flush()
            with fitz.open(tmp.name) as doc:
                return "\n".join(page.get_text() for page in doc)
    elif ext == "xlsx":
        df = pd.read_excel(file)
        return df.to_string(index=False)
    return ""

def semantic_search_faq(question, threshold=0.5):
    normalized_question = normalize(question)
    q_embedding = model.encode(normalized_question, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(q_embedding, faq_embeddings)[0]
    best_score = cos_scores.max().item()
    if best_score >= threshold:
        best_idx = cos_scores.argmax().item()
        answer = faq_data[faq_questions[best_idx]].strip()
        if answer.lower() in ["", "nan", "none"]:
            return "__VIDE__"
        return answer
    return None

def show_logo(path):
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"<div style='text-align:center'><img src='data:image/png;base64,{encoded}' width='190'></div>", unsafe_allow_html=True)

show_logo("SEGULA_Technologies_logo_DB.jpg")
st.markdown("<h2 style='text-align:center; color:#1e88e5;'>🤖 Chatbot RH SEGULA Technologies</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "content": "👋 Bonjour ! Posez votre question  ou téléversez un fichier."}]
if "doc_content" not in st.session_state:
    st.session_state.doc_content = ""

if st.button("🗑️ Vider la conversation"):
    st.session_state.messages = [{"role": "bot", "content": "👋 Bonjour ! Posez votre question ou téléversez un fichier."}]
    st.session_state.doc_content = ""
    st.rerun()

uploaded_file = st.file_uploader("📎 Téléverser un document (PDF, TXT, Excel)", type=["pdf", "txt", "xlsx"])
if uploaded_file:
    st.session_state.doc_content = extract_file_content(uploaded_file)
    st.success("✅ Fichier chargé avec succès")

for msg in st.session_state.messages:
    align = "margin-left:auto;" if msg["role"] == "user" else "margin-right:auto;"
    bg = "#1e88e5" if msg["role"] == "user" else "#f1f1f1"
    color = "#fff" if msg["role"] == "user" else "#000"
    label = "👩‍💼 Vous" if msg["role"] == "user" else "🤖 Bot"
    st.markdown(f"""
    <div style='background:{bg}; color:{color}; padding:10px 15px;
                border-radius:12px; margin:10px 0; max-width:75%; {align}'>{label}: {msg['content']}</div>
    """, unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Tapez votre question ici...")
    submitted = st.form_submit_button("Envoyer")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    clean_input = normalize(user_input)
    response = semantic_search_faq(clean_input)

    if response == "__VIDE__":
        response = "❗ La question existe dans la FAQ, mais la réponse n’a pas encore été renseignée par le service RH."
        st.session_state.messages.append({"role": "bot", "content": response})
        st.rerun()

    if not response:
        with st.spinner("✍️ Je rédige la réponse…"):
            prompt = user_input
            if st.session_state.doc_content:
                limited_doc = " ".join(st.session_state.doc_content.split()[:1000])
                prompt = f"""Voici un extrait d’un document RH :\n\n\"\"\"{limited_doc}\"\"\"\n\nQuestion RH d’un employé : {user_input}\nRéponds de façon claire et directe."""
                st.info("❗ Réponse non disponible dans la FAQ. Je vais demander à Gemini…")
            else:
                prompt = f"Question RH d’un employé : {user_input}\nRéponds de façon claire et directe."
            response = ask_gemini(prompt)

    st.session_state.messages.append({"role": "bot", "content": response})
    st.rerun()

def save_chat_history():
    df = pd.DataFrame([
        {"Rôle": m["role"], "Message": m["content"], "Horodatage": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        for m in st.session_state.messages
    ])
    df.to_excel("chat_segula_log.xlsx", index=False)

save_chat_history()

if os.path.exists("chat_segula_log.xlsx"):
    with open("chat_segula_log.xlsx", "rb") as f:
        st.download_button("📥 Télécharger l'historique", f, file_name="chat_segula_log.xlsx")
