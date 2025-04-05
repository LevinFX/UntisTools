import streamlit as st
import os
import json
import requests

st.set_page_config(
    page_title="Schüler",
    page_icon="👨‍🎓",
)

# Datenabruf
@st.cache_data(ttl=3600000)
def load_students():
    try:
        response = requests.get("http://127.0.0.1:5000/api/students")
        return response.json()
    except Exception as e:
        st.error(f"Daten konnten nicht geladen werden: {str(e)}")
        return {'students': []}

# Main page content
st.title("👨‍🎓 Schüler")

#spacing
st.markdown("###")

students = load_students()

# Stats
for student in students:
        with st.expander(student['foreName'] +' - '+ student['longName']):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown(f"**🏷️ Voller Name:** {student['foreName']} {student['longName']}")
                st.markdown(f"**🪪 Id:** {student.get('id', 'Unbekannt')}")
                
            with col2:
                # Sicherer Zugriff mit Fallback
                gender = student.get('gender')
                # Case-insensitive Prüfung
                emoji = "👨‍🎓" if gender.lower() == "male" else "👩‍🎓"
                # Kapitalisierung erst nach Sicherstellung eines validen Strings
                st.markdown(f"**{emoji} Geschlecht:** {student['gender']}")