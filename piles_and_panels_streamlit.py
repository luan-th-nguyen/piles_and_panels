import streamlit as st
import numpy as np
from src.main_secant_piled_shaft import main_secant_piled_shaft
from src.main_secant_piled_wall import main_secant_piled_wall
from src.main_diaphragm_panel_shaft import main_diaphragm_panel_shaft
from src.main_diaphragm_panel_wall import main_diaphragm_panel_wall


st.set_page_config(page_title='Secant piled shaft/ wall', page_icon=":eyeglasses:")


# Sidebar
st.sidebar.markdown('# Form selection')
select_event = st.sidebar.selectbox('Select one of the form', ['Secant piled shaft', 'Secant piled wall', 'Diaphragm panel shaft', 'Diaphragm panel wall'])

if select_event == 'Secant piled shaft':
    main_secant_piled_shaft(st)

elif select_event == 'Secant piled wall':
    main_secant_piled_wall(st)

elif select_event == 'Diaphragm panel shaft':
    main_diaphragm_panel_shaft(st)

else:
    main_diaphragm_panel_wall(st)
