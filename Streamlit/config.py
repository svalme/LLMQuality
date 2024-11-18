# Define your themes

import streamlit as st

themes = {
    "current_theme": "dark",
    "refreshed": True,
    "light": {
        "theme.base": "dark",
        "theme.primaryColor": "#F63366",
        "theme.backgroundColor": "#FFFFFF",
        "theme.secondaryBackgroundColor": "#F0F2F6",
        "theme.textColor": "#262730",
        "button_face": "🌞"
    },
    "dark": {
        "theme.base": "light",
        "theme.primaryColor": "#b4b4b4",
        "theme.backgroundColor": "#212121",
        "theme.secondaryBackgroundColor": "#0E1117",
        "theme.textColor": "#9d9d9d",
        "button_face": "🌜"
    }
}

themes2 = {
            "current_theme": "light",
            "refreshed": True,
            "light": {
                "theme.base": "dark",
                "theme.backgroundColor": "black",
                "theme.primaryColor": "#c98bdb",
                "theme.secondaryBackgroundColor": "#5591f5",
                "theme.textColor": "white",
                "button_face": "🌜"
            },
            "dark": {
                "theme.base": "light",
                "theme.backgroundColor": "white",
                "theme.primaryColor": "#5591f5",
                "theme.secondaryBackgroundColor": "#82E1D7",
                "theme.textColor": "#0a1464",
                "button_face": "🌞"
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
    if previous_theme == "dark":
        st.session_state.themes["current_theme"] = "light"
    elif previous_theme == "light":
        st.session_state.themes["current_theme"] = "dark"

def theme_selection():
    btn_face = st.session_state.themes["light"]["button_face"] if st.session_state.themes["current_theme"] == "light" else \
        st.session_state.themes["dark"]["button_face"]
    st.button(btn_face, on_click=change_theme)

    if st.session_state.themes["refreshed"] == False:
        st.session_state.themes["refreshed"] = True
        st.rerun()