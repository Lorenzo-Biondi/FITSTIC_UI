import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
#pages in python format
from pages import penguins, titanic, diabetes

st.set_page_config(
                    page_title="Template Project",
                    page_icon=str('🤖'),
                    layout="wide",
                    )

page = [
        "Penguins", 
        "Titanic",
        "Diabetes"
        ]

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
                        "title": title,
                        "function": function
                        })

    def main():
        with st.sidebar:
            app = option_menu(
                            menu_title = "Menu",
                            options = page,
                            #orientation = "horizontal",
                            menu_icon = "bi-list",
                            default_index = 0,
                            styles = {
                                    "container": {"padding": "5!important", "background-color": "black"},
                                    "icon": {"color": "white", "font-size": "23px"},
                                    "nav-link": {"color": "white", "font-size": "20 px", "text-align": "left", "margin": "0px" },
                                    "nav-link-selected": {"color": "black", "background-color": "#9ac280"}
                                    }
                            )
        if app == page[0]:
            penguins.main()
        if app == page[1]:
            titanic.main()
        if app == page[2]:
            diabetes.main()