import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Lade die Umgebungsvariablen
load_dotenv()

# Konfiguriere OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title("Chatbot mit OpenAI")

# Session State für die Chatgeschichte
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat-Geschichte anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Was möchtest du wissen?"):
    # User Nachricht speichern
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Chat-Geschichte aktualisieren
    with st.chat_message("user"):
        st.markdown(prompt)

    # Antwort von OpenAI generieren
    with st.chat_message("assistant"):
        with st.spinner("Denke nach..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
                        *st.session_state.messages
                    ]
                )
                assistant_response = response.choices[0].message.content
                st.markdown(assistant_response)
                
                # Antwort speichern
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            except Exception as e:
                st.error(f"Fehler beim Generieren der Antwort: {str(e)}")
