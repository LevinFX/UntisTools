import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(
    page_title="Stundenplan",
    page_icon="📅",
    layout="wide"
)

# Hilfsfunktionen
def safe_get(lst, index, key, default="?"):
    """Sicherer Zugriff auf verschachtelte Listen/Dictionaries"""
    try:
        return lst[index].get('element', {}).get(key, default)
    except (IndexError, KeyError, TypeError):
        return default

def format_time(time_int):
    """Formatiert die Zeitangabe in HH:MM"""
    try:
        time_str = f"{time_int:04d}"
        return f"{time_str[:2]}:{time_str[2:]}"
    except:
        return ""

def format_date(date_int):
    """Formatiert das Datum in DD.MM.YYYY"""
    try:
        return datetime.strptime(str(date_int), "%Y%m%d").strftime("%a %d.%m.%Y")
    except:
        return "Unbekanntes Datum"

# Datenabruf
@st.cache_data(ttl=3600)
def load_timetable():
    try:
        response = requests.get("http://127.0.0.1:5000/api/Timetable")
        return response.json()
    except Exception as e:
        st.error(f"Daten konnten nicht geladen werden: {str(e)}")
        return []

timetable_data = load_timetable()

# Rest des Codes bleibt gleich wie zuvor...

# In der create_schedule_grid Funktion:
def create_schedule_grid(lessons):
    time_slots = sorted({
        f"{format_time(l['startTime'])}-{format_time(l['endTime'])}" 
        for l in lessons
    }, key=lambda x: x.split('-')[0].replace(':', ''))

    dates = sorted({
        format_date(l['date']) for l in lessons 
        if l.get('date')
    }, key=lambda x: datetime.strptime(x.split(' ')[-1], "%d.%m.%Y"))

    grid = pd.DataFrame(index=time_slots, columns=dates)

    for lesson in lessons:
        date = format_date(lesson.get('date'))
        time_slot = f"{format_time(lesson.get('startTime'))}-{format_time(lesson.get('endTime'))}"
        
        subject = safe_get(lesson.get('subjects', []), 0, 'displayname', '?')
        teacher = safe_get(lesson.get('teachers', []), 0, 'name', '?')
        room = safe_get(lesson.get('rooms', []), 0, 'displayname', '?')
        
        entry = f"{subject}\n{teacher}\n{room}"
        
        if lesson.get('is', {}).get('cancelled'):
            entry += "\n❌"
        elif lesson.get('is', {}).get('substitution'):
            entry += "\n🔄"
        
        grid.at[time_slot, date] = entry

    return grid.fillna("–").reset_index().rename(columns={'index': 'Uhrzeit'})

def apply_grid_styling(df):
    def color_cells(val):
        styles = []
        if '❌' in val:
            styles.append('background-color: #808080; color: white;')
        if '🔄' in val:
            styles.append('background-color: #6C3BAA; color: white')
        return ' '.join(styles)
    
    return df.style.applymap(color_cells).set_properties(**{
        'white-space': 'pre-wrap',
        'border': '1px solid #dee2e6',
        'text-align': 'center',
        'vertical-align': 'middle'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#f0f2f6'),
                 ('position', 'sticky'),
                 ('left', '0'),
                 ('top', '0')]
    }])
# Erweiterte Ansicht
def display_detailed_view(lessons):
    def safe_get(lst, index, key, default="?"):
        try:
            return lst[index].get('element', {}).get(key, default)
        except (IndexError, KeyError, TypeError):
            return default

    for lesson in lessons:
        subject = safe_get(lesson.get('subjects', []), 0, 'displayname', 'Fach')
        room = safe_get(lesson.get('rooms', []), 0, 'displayname', 'Raum')
        
        with st.expander(f"{subject} - {room}"):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown(f"**📅 Datum:** {format_date(lesson.get('date'))}")
                st.markdown(f"**⏰ Zeit:** {format_time(lesson.get('startTime'))} - {format_time(lesson.get('endTime'))}")
                st.markdown(f"**👨🏫 Lehrer:** {safe_get(lesson.get('teachers', []), 0, 'name', 'Kein Lehrer')}")
                st.markdown(f"**🏫 Raum:** {room}")
                
            with col2:
                if lesson.get('periodText'):
                    st.warning(f"ℹ️ {lesson['periodText']}")
                if lesson.get('exam'):
                    st.error(f"📝 Prüfung: {lesson['exam'].get('name', 'Unbenannte Prüfung')}")
                if lesson.get('is', {}).get('substitution'):
                    st.info("🔄 Vertretungsstunde")
                if lesson.get('is', {}).get('cancelled'):
                    st.error("❌ Stunde entfällt")

            classes = ", ".join([safe_get(lesson.get('classes', []), i, 'displayname') 
                               for i in range(len(lesson.get('classes', [])))])
            if classes:
                st.caption(f"🎒 Klassen: {classes}")

# Hauptprogramm
st.title("📅 Stundenplan")
view_mode = st.radio("Ansichtsmodus:", 
                    ["Detailansicht", "Stundenplan-Format"], 
                    horizontal=True,
                    label_visibility="collapsed")

if not timetable_data:
    st.warning("Keine Stundenplandaten verfügbar")
    st.stop()

if view_mode == "Detailansicht":
    dates = sorted(set(l.get('date') for l in timetable_data), key=lambda x: x or 0)
    for date in dates:
        st.subheader(format_date(date))
        daily_lessons = [l for l in timetable_data if l.get('date') == date]
        daily_lessons.sort(key=lambda x: x.get('startTime', 0))
        display_detailed_view(daily_lessons)
else:
    grid = create_schedule_grid(timetable_data)
    styled_grid = apply_grid_styling(grid)
    
    st.markdown("""
    <style>
        [data-testid="stDataFrame"] {
            max-height: 80vh;
            overflow: auto;
        }
        .stDataFrame th {
            position: -webkit-sticky;
            position: sticky;
            top: 0;
            z-index: 1;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        styled_grid,
        use_container_width=True,
        hide_index=True,
        height=450
    )