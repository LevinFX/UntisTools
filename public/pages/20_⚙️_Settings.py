import streamlit as st
import json
import os

SETTINGS_FILE = 'settings.json'

def load_settings():
    """Lädt gespeicherte Einstellungen mit Defaults für URL und Schule"""
    default_settings = {
        'untis_user': '',
        'untis_password': '',
        'untis_url': 'hektor.webuntis.com',
        'untis_school': 'Zum_Dom',
        'phone_number': ''
    }
    
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            loaded = json.load(f)
            # Merge mit Defaults falls neue Felder hinzukommen
            return {**default_settings, **loaded}
    return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def main():
    st.title("Einstellungen")
    settings = load_settings()

    with st.form("settings_form"):
        st.subheader("Untis Zugangsdaten")
        untis_user = st.text_input("Benutzername", value=settings['untis_user'])
        untis_password = st.text_input("Passwort", type='password', value=settings['untis_password'])
        untis_url = st.text_input("Server URL", value=settings['untis_url'])
        untis_school = st.text_input("Schule", value=settings['untis_school'])
        
        st.subheader("Kontaktinformationen")
        phone_number = st.text_input("Telefonnummer", value=settings['phone_number'])

        submitted = st.form_submit_button("Einstellungen speichern")

    if submitted:
        if not untis_user or not untis_password or not untis_url or not untis_school:
            st.error("Bitte fülle alle Pflichtfelder aus (Benutzername, Passwort, URL, Schule)")
            return

        new_settings = {
            'untis_user': untis_user,
            'untis_password': untis_password,
            'untis_url': untis_url,
            'untis_school': untis_school,
            'phone_number': phone_number
        }

        save_settings(new_settings)
        st.session_state.update(new_settings)
        st.success("Einstellungen erfolgreich gespeichert!")

if __name__ == "__main__":
    main()