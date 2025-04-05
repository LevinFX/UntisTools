import streamlit as st
import os
import json
import requests

st.set_page_config(
    page_title="Klassen",
    page_icon="👥",
)

# Datenabruf
@st.cache_data(ttl=3600)
def load_classes():
    try:
        response = requests.get("http://127.0.0.1:5000/api/classes")
        return response.json()
    except Exception as e:
        st.error(f"Daten konnten nicht geladen werden: {str(e)}")
        return {'classes': []}

# Main page content
st.title("👥 Klassen")

#spacing
st.markdown("###")

classes = load_classes()

# Stats
for c in classes:
        with st.expander(c['name']):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown(f"**🏷️ Langer Name:** {c.get('longName', "Unbekannt")}")
                st.markdown(f"**👤 LehrerId:** {c.get('teacher1', 'Unbekannt')}")
                
            with col2:
                st.markdown(f"**🪪 Id:** {c['id']}")