import streamlit as st
import numpy as np
from src.main_secant_piled_shaft import main_secant_piled_shaft
from src.main_secant_piled_wall import main_secant_piled_wall
from src.main_diaphragm_panel_shaft import main_diaphragm_panel_shaft
from src.main_diaphragm_panel_wall import main_diaphragm_panel_wall
from src.file_utilitites import (st_json_download_button, assign_session_state_parameters_wall_secant_piles,
                                 assign_session_state_parameters_shaft_secant_piles,assign_session_state_parameters_shaft_diaphragm_panels,
                                 assign_session_state_parameters_wall_diaphragm_panels)#, export_as_pdf)
from src.file_utilitites import load_parameters_from_json_file


st.set_page_config(page_title='Secant piled shaft/ wall', page_icon=":eyeglasses:")


parameters_user = None

# Load section state
st.sidebar.header('Load saved session state (optional)')
uploaded_file_session_state = st.sidebar.file_uploader('Select session state file to load', type='json')
if uploaded_file_session_state is not None:
    try:
        parameters_user = load_parameters_from_json_file(uploaded_file_session_state)
        st.sidebar.success('File successfully loaded')
    except Exception as e:
        st.sidebar.error(e)

# Sidebar
st.sidebar.markdown('# Form selection')
select_options = ['Secant piled shaft', 'Secant piled wall', 'Diaphragm panel shaft', 'Diaphragm panel wall']
if parameters_user is not None:
    select_event = st.sidebar.selectbox('Select one of the form', select_options, index=select_options.index(parameters_user['selected_form']), key='selected_form')
    if parameters_user['selected_form'] == 'Secant piled shaft':
        parameters_user = assign_session_state_parameters_shaft_secant_piles(**parameters_user)

    elif parameters_user['selected_form'] == 'Secant piled wall':
        parameters_user = assign_session_state_parameters_wall_secant_piles(**parameters_user)

    elif parameters_user['selected_form'] == 'Diaphragm panel shaft':
        parameters_user = assign_session_state_parameters_shaft_diaphragm_panels(**parameters_user)

    elif parameters_user['selected_form'] == 'Diaphragm panel wall':
        parameters_user = assign_session_state_parameters_wall_diaphragm_panels(**parameters_user)

    else:
        pass
else:
    select_event = st.sidebar.selectbox('Select one of the form', select_options, key='selected_form')

if select_event == 'Secant piled shaft':
    main_secant_piled_shaft(st, parameters_user)

elif select_event == 'Secant piled wall':
    main_secant_piled_wall(st, parameters_user)

elif select_event == 'Diaphragm panel shaft':
    main_diaphragm_panel_shaft(st)

elif select_event == 'Diaphragm panel wall':
    main_diaphragm_panel_wall(st)

else:
    pass


# Save section state
st.sidebar.header('Report and save session state')
#figs = [fig1, fig2]

button_print_report = st.sidebar.button('Export PDF', key='export_pdf_sps')
if button_print_report:
    st.sidebar.write('Not yet implemented! Please use the browser printing function for now.')
    #export_as_pdf(fig1)

# Download session state JSON file
session_state = dict(st.session_state)  # LazySessionState to dict

download_filename = 'piles_and_pannels' + '.JSON'
href = st_json_download_button(session_state, download_filename)
st.sidebar.markdown(href, unsafe_allow_html=True)

# Notes
st.sidebar.header('Version')
st.sidebar.write('nya.2021.09')
