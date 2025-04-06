import streamlit as st
import os
import json
import requests

st.set_page_config(
    page_title="Lehrer",
    page_icon="🧑‍🏫",
)

# Datenabruf
@st.cache_data(ttl=3600000)
def load_teachers():
    try:
        response = requests.get("http://127.0.0.1:5000/api/teachers")
        return response.json()
    except Exception as e:
        st.error(f"Daten konnten nicht geladen werden: {str(e)}")
        return {'teachers': []}

# Main page content
st.title("🧑‍🏫 Lehrer")

#spacing
st.markdown("###")

teachers = load_teachers()

# Stats
for teacher in teachers:
        with st.expander(teacher.get('foreName', 'Unbekannt') +' - '+ teacher.get('longName', 'Unbekannt')):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown(f"**🏷️ Voller Name:** {teacher.get('foreName', 'Unbekannt')} {teacher.get('longName', 'Unbekannt')}")
                st.markdown(f"**🏷️ Handle:** {teacher.get('name', 'Unbekannt')}")
                st.markdown(f"**🪪 Id:** {teacher.get('id', 'Unbekannt')}")
                
            with col2:
                # Sicherer Zugriff mit Fallback
                firstname = teacher.get('foreName', 'error').lower() or "error"
                mail = teacher.get('longName', 'Unbekannt').lower() + firstname[0] if firstname else ''
                # Case-insensitive Prüfung
                # Kapitalisierung erst nach Sicherstellung eines validen Strings
                st.markdown(f"**📧 Email: ** {mail}@luebeck.schule")