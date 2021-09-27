import numpy as np
from src.shaft_diaphragm_panels import (get_parameters_shaft_diaphragm_panels, plot_wall_diaphragm_panels)
from src.file_utilitites import (st_json_download_button, load_parameters_from_json_file_dw)#, export_as_pdf)

def main_diaphragm_panel_wall(st):
    """Main form for diagragm panel wall

    Args:
        st (streamlit): A streamlit object
    """
    st.title('Geometric check for diaphragm panel wall')
    st.subheader('(Version 2021.09)')
    # Initial parameters
    parameters = {"project_name_dw": "Sample project", "project_revision_dw": "First issue, rev0", "wall_name_dw": "Wall 1", "D_dw": 1.2,
                "B_dw": 2.8, "L_dw": 35.0, "v_dw": 0.5, "H_drilling_platform_dw": 0.0}

    st.header('Load saved session state (optional)')
    uploaded_file_session_state = st.file_uploader('Select session state file to load', type='json')
    if uploaded_file_session_state is not None:
        try:
            #breakpoint()
            parameters = load_parameters_from_json_file_dw(uploaded_file_session_state)
            st.success('File successfully loaded')
        except Exception as e:
            st.error(e)

    st.header('Project information')
    project_name = st.text_input('Project', value=parameters['project_name_dw'], key='project_name_dw')
    st.text_input('Revision', value=parameters['project_revision_dw'], key='project_revision_dw')


    st.header('Input parameters')
    col1, col2, col3 = st.columns(3)
    wall_name = col1.text_input('Wall identification', value=parameters['wall_name_dw'], key='wall_name_dw')
    #di = col1.number_input('Shaft inner diameter [m]', value=parameters['di_dws'], format='%.2f', min_value=1.0, max_value=100.0, step=1.0, key='di_dws')
    D = col2.number_input('Pannel thickness [m]', value=parameters['D_dw'], format='%.2f', min_value=0.3, max_value=5.0, step=0.1, key='D_dw')
    B = col3.number_input('Pannel length (for plotting) [m]', value=parameters['B_dw'], format='%.2f', min_value=0.3, max_value=15.0, step=0.1, key='B_dw')
    #n_pieces = int(col3.number_input('Numer of pannels [-]', value=int(parameters['n_pieces_dws']), format='%i', min_value=4, max_value=1000, step=1, key='n_pieces_dws'))
    L = col1.number_input('Length of wall [m]', value=parameters['L_dw'], step=1.0,min_value=1.0, max_value=150.0, key='L_dw')
    v = col2.number_input('Drilling verticality [%]', value=parameters['v_dw'], step=0.1, min_value=0.05, max_value=2.0, key='v_dw')
    col1, col2 = st.columns(2)
    H_drilling_platform = col1.number_input('Height of drilling platform above top of panels [m]', value=parameters['H_drilling_platform_dw'], step=1.0, min_value=0.0, max_value=20.0, key='H_drilling_platform_dw')
    col2.write('The initial devivation by free drilling x0 = {:.2f} cm'.format(H_drilling_platform*v))

    x0, x, d_eff = get_parameters_shaft_diaphragm_panels(D, L, H_drilling_platform, v)

    st.header('Output parameters for {}'.format(wall_name))
    col1, col2 = st.columns(2)
    col1.write('Deviation at bottom of shaft dx = {:.2f} cm'.format(x*100))
    col1.write('Effective pannel thickness at bottom of shaft d_eff = {:.2f} cm'.format(d_eff*100))
    if d_eff <= 0:
        col2.warning('PANELS DO NOT TOUCH IN BASE OF WALL!!')

    st.header('Visualization for {}'.format(wall_name))
    fig1 = plot_wall_diaphragm_panels(2, D, B, x0, x, wall_name)
    st.pyplot(fig1)


    # Save section state
    st.header('Report and save session state')
    #figs = [fig1, fig2]

    button_print_report = st.button('Export PDF', key='export_pdf_sps')
    if button_print_report:
        st.write('Not yet implemented!')
        #export_as_pdf(fig1)

    # Download session state JSON file
    session_state = dict(st.session_state)  # LazySessionState to dict

    download_filename = 'wall_diaphragm_panels_' + project_name + '.JSON'
    st_json_download_button(session_state, download_filename)
