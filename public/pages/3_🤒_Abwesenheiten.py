import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Abwesenheiten",
    page_icon="🤒",
    layout="wide"
)

# Hilfsfunktionen
def format_time(time_int):
    """Formatiert die Zeitangabe in HH:MM"""
    try:
        return f"{str(time_int)[:-2]}:{str(time_int)[-2:]}" if time_int > 0 else ""
    except:
        return ""

def format_date(date_int):
    """Formatiert das Datum in DD.MM.YYYY"""
    try:
        return datetime.strptime(str(date_int), "%Y%m%d").strftime("%d.%m.%Y")
    except:
        return "Unbekanntes Datum"

# Datenabruf
@st.cache_data(ttl=3600)
def load_absent():
    try:
        response = requests.get("http://127.0.0.1:5000/api/absent")
        return response.json()
    except Exception as e:
        st.error(f"Daten konnten nicht geladen werden: {str(e)}")
        return {'absences': []}

# Hauptprogramm
st.title("🤒 Abwesenheiten")
st.markdown("###")

absent_data = load_absent()

if not absent_data.get('absences'):
    st.info("Keine Abwesenheiten gefunden")
    st.stop()

# Gruppiere nach Datum
dates = sorted({abs['startDate'] for abs in absent_data['absences']}, reverse=True)

for date in dates:
    st.subheader(format_date(date))
    
    # Filtere Einträge für dieses Datum
    daily_absences = [abs for abs in absent_data['absences'] if abs['startDate'] == date]
    
    for absence in daily_absences:
        with st.expander(f"{format_time(absence['startTime'])} - {format_time(absence['endTime'])} | {absence.get('reason', 'Kein Grund angegeben')}"):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown(f"**📅 Datum:** {format_date(absence['startDate'])}")
                if absence['startDate'] != absence['endDate']:
                    st.markdown(f"**Bis:** {format_date(absence['endDate'])}")
                
                st.markdown(f"**⏰ Uhrzeit:** {format_time(absence['startTime'])} - {format_time(absence['endTime'])}")
                st.markdown(f"**👤 Erfasst von:** {absence.get('createdUser', 'Unbekannt')}")
                
            with col2:
                # Sicherer Zugriff mit Fallback
                status = absence.get('excuseStatus') or 'nicht entschuldigt'
                # Case-insensitive Prüfung
                color = "🟢" if status.lower() == "entschuldigt" else "🔴"
                # Kapitalisierung erst nach Sicherstellung eines validen Strings
                st.markdown(f"**{color} Status:** {status.capitalize()}")
                    
                if absence.get('text'):
                    st.markdown(f"**📝 Grund:** {absence['text']}")
                
                if absence.get('excuse', {}).get('text'):
                    st.markdown(f"**📄 Entschuldigungstext:**")
                    st.write(absence['excuse']['text'])

            # Zusätzliche Informationen
            if absence.get('isExcused'):
                st.success("Diese Abwesenheit ist entschuldigt")
            else:
                st.warning("Diese Abwesenheit ist noch nicht entschuldigt")