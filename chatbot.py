
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq


# ==========================================
# 1. CONFIGURATION
# ==========================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Gen AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. DESIGN CSS - BLACK & WHITE THEME
# ==========================================

st.markdown("""
<style>

/* Background general */
.stApp {
    background-color: #000000;
    color: #FFFFFF;
}

/* Textes */
html, body, [class*="css"],
p, span, label, li {
    color: #FFFFFF !important;
}

/* Titres */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
}

/* Titre principal */
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    color: #FFFFFF !important;
    margin-bottom: 5px;
}

/* Sous-titre */
.subtitle {
    text-align: center;
    color: #CCCCCC !important;
    font-size: 15px;
    margin-bottom: 30px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #000000;
    border-right: 1px solid #333333;
}

/* Zone principale */
section[data-testid="stMain"] {
    background-color: #000000;
}

/* Messages */
[data-testid="stChatMessage"] {
    background-color: #111111;
    border: 1px solid #333333;
    border-radius: 12px;
    padding: 15px;
}

/* Zone de saisie */
[data-testid="stChatInput"] {
    background-color: #111111;
    border: 1px solid #444444;
    border-radius: 12px;
}

[data-testid="stChatInput"] textarea {
    color: #FFFFFF !important;
    background-color: #111111 !important;
    caret-color: #FFFFFF;
}

/* Boutons */
.stButton button {
    background-color: #222222;
    color: #FFFFFF !important;
    border: 1px solid #555555;
    border-radius: 10px;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #444444;
    border-color: #FFFFFF;
    color: #FFFFFF !important;
}

/* Séparateurs */
hr {
    border-color: #444444;
}

/* Notifications */
[data-testid="stAlert"] {
    background-color: #151515;
    color: #FFFFFF;
}

/* Liens */
a {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🤖 Gen AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent AI assistant powered by Groq & LangChain'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 4. INITIALISATION DE L'HISTORIQUE
# ==========================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================
# 5. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("### Model information")

    st.success("🟢 Groq API")

    st.info("Model: GPT-OSS 20B")

    st.caption("Powered by LangChain")

    st.divider()

    st.markdown("### Conversation")

    st.write(
        f"Messages: {len(st.session_state.chat_history)}"
    )

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):

        st.session_state.chat_history = []
        st.rerun()

    st.divider()

    st.caption("Gen AI Chatbot | Version 1.0")


# ==========================================
# 6. VERIFICATION DE LA CLE API
# ==========================================

if not api_key:

    st.error(
        "GROQ_API_KEY introuvable. "
        "Vérifie ton fichier .env."
    )

    st.stop()


# ==========================================
# 7. INITIALISATION DU MODELE LLM
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
    api_key=api_key
)


# ==========================================
# 8. AFFICHAGE DE L'HISTORIQUE
# ==========================================

if not st.session_state.chat_history:

    st.markdown("### 👋 Welcome!")

    st.write(
        "Hello! I'm your AI assistant. "
        "Ask me anything and let's start a conversation."
    )


for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# 9. INPUT UTILISATEUR
# ==========================================

user_prompt = st.chat_input(
    "💬 Ask me anything..."
)


# ==========================================
# 10. GENERATION DE LA REPONSE
# ==========================================

if user_prompt:

    # Afficher le message utilisateur
    with st.chat_message("user"):

        st.markdown(user_prompt)

    # Ajouter le message utilisateur à l'historique
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    try:

        with st.chat_message("assistant"):

            with st.spinner("🤔 AI is thinking..."):

                # Définir le system prompt
                messages = [
                    (
                        "system",
                        "You are a helpful AI assistant. "
                        "Answer clearly and accurately."
                    )
                ]

                # Ajouter l'historique de conversation
                for message in st.session_state.chat_history:

                    messages.append((
                        message["role"],
                        message["content"]
                    ))

                # Envoyer les messages au modèle
                response = llm.invoke(messages)

                assistant_response = response.content

            # Afficher la réponse
            st.markdown(assistant_response)

        # Enregistrer la réponse
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": assistant_response
        })

    except Exception as e:

        st.error(
            f"An error occurred: {str(e)}"
        )

