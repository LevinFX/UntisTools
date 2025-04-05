import streamlit as st
import os
import json
import requests
from datetime import datetime
import html

st.set_page_config(
    page_title="Dashboard",
    page_icon="💻",
)

def load_settings():
    """Lädt gespeicherte Einstellungen mit Defaults für URL und Schule"""
    default_settings = {
        'untis_user': 'Benutzer',
    }
    
    if os.path.exists("settings.json"):
        with open("settings.json", 'r') as f:
            loaded = json.load(f)
            # Merge mit Defaults falls neue Felder hinzukommen
            return {**default_settings, **loaded}
    return default_settings

settings = load_settings()

# Datenabruf
@st.cache_data(ttl=3600)
def load_data():
    try:
        response = requests.get("http://127.0.0.1:5000/api/data")
        return response.json()
    except Exception as e:
        st.error(f"Daten konnten nicht geladen werden: {str(e)}")
        return {'data': []}


@st.cache_data(ttl=3600)
def load_motd():
    try:
        response = requests.get("http://127.0.0.1:5000/api/motd")
        data = response.json()
        return data.get('messagesOfDay', [])
    except Exception as e:
        st.error(f"MOTD konnten nicht geladen werden: {str(e)}")
        return []

# Main page content
st.title("💻 Dashboard")

st.text("Hello, "+ settings["untis_user"].split(sep=".")[0]+" 👋")

#spacing
st.markdown("###")

data = load_data()

# Stats
ausfall, vertretung, hausaufgaben, arbeiten = st.columns(4)

ausfall.metric("Ausfall", data[0].get("current"), data[0].get("difference"))
vertretung.metric("Vertretung", data[1].get("current"), data[1].get("difference"))
hausaufgaben.metric("Arbeiten", data[2].get("current"), data[2].get("difference"))
arbeiten.metric("Hausaufgaben", data[3].get("current"), data[3].get("difference"))

#spacing
st.markdown("###")

# MOTD Section
st.markdown("### 📢 Messages of the Day")
motds = load_motd()

if not motds:
    st.info("Keine aktuellen Nachrichten")
else:
    for motd in motds:
        subject = motd.get('subject', 'Ohne Betreff')
        text = motd.get('text', 'Kein weiterer Text')
        
        # HTML-Tags entfernen und Zeilenumbrüche formatieren
        cleaned_text = html.unescape(text)  # HTML-Entities konvertieren
        cleaned_text = cleaned_text.replace('<div>', '\n').replace('</div>', '')
        cleaned_text = cleaned_text.replace('<br />', '\n')
        
        with st.expander(f"📌 {subject}"):
            st.markdown(f"**{subject}**")
            if cleaned_text.strip():
                st.markdown(cleaned_text)
            else:
                st.caption("Kein zusätzlicher Text vorhanden")