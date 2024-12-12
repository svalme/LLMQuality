# Define your themes

import streamlit as st

themes = {
    "current_theme": "light",
    "refreshed": True,
    "light": {
        "theme.base": "dark",
        "theme.primaryColor": "#000000",
        "theme.backgroundColor": "#FFFFFF",
        "theme.secondaryBackgroundColor": "#F0F2F6",
        "theme.textColor": "#0D0D0D",
        "button_face": "🌞",
        "containerBackground": "#F3F3F3"
    },
    "dark": {
        "theme.base": "light",
        "theme.primaryColor": "#b4b4b4",
        "theme.backgroundColor": "#212121",
        "theme.secondaryBackgroundColor": "#0E1117",
        "theme.textColor": "#ECECEC",
        "button_face": "🌜",
        "containerBackground": "#303030"
    }
}



# Function to change theme
def change_theme():
    previous_theme = st.session_state.themes["current_theme"]
    tdict = st.session_state.themes["light"] if st.session_state.themes["current_theme"] == "light" else \
        st.session_state.themes["dark"]
    for vkey, vval in tdict.items():
        if vkey.startswith("theme"):
            st._config.set_option(vkey, vval)
    st.session_state.themes["refreshed"] = False
    st.session_state.themes["current_theme"] = "light" if previous_theme == "dark" else "dark"
    st.session_state.current_theme = st.session_state.themes["current_theme"]



def theme_selection():
    btn_face = st.session_state.themes["light" if st.session_state.themes["current_theme"] == "light" else "dark"][
        "button_face"]
    st.button(btn_face, on_click=change_theme)
    if not st.session_state.themes["refreshed"]:
        st.session_state.themes["refreshed"] = True
        st.rerun()

def initialize_theme():
    current_theme = st.session_state.themes["current_theme"]
    theme_dict = st.session_state.themes[current_theme]
    for vkey, vval in theme_dict.items():
        if vkey.startswith("theme"):
            st._config.set_option(vkey, vval)

def apply_theme_to_question():
    current_theme = themes[st.session_state.current_theme]
    st.markdown(f"""
        <style>
            .my-container {{
                background-color: {current_theme["containerBackground"]};
                color: {current_theme["theme.textColor"]};
                border-radius: 10px;
                padding: 10px;
            }}
        </style>
    """, unsafe_allow_html=True)


