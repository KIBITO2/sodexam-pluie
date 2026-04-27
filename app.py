import streamlit as st

from config import APP_TITLE, PAGE_ICON, LAYOUT
from services.storage import init_storage
from ui.login_page import render_login
from ui.sidebar import render_sidebar
from ui.carte_page import render_carte_page
from ui.saisie_page import render_saisie_page
from ui.historique_page import render_historique_page
from ui.dashboard_page import render_dashboard_page
from ui.comptes_page import render_comptes_page


def init_session_state():
    defaults = {
        "connecte": False,
        "username": "",
        "role": "",
        "ville": "",
        "email": "",
        "zip_path": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

    init_storage()
    init_session_state()

    if not st.session_state["connecte"]:
        render_login()
        return

    page = render_sidebar()

    if page == "Carte Nationale":
        render_carte_page()
    elif page == "Saisie Relevé":
        render_saisie_page()
    elif page == "Historique":
        render_historique_page()
    elif page == "Dashboard Admin":
        render_dashboard_page()
    elif page == "Gestion des Comptes":
        render_comptes_page()


if __name__ == "__main__":
    main()
