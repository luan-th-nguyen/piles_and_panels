import numpy as np
from src.shaft_diaphragm_panels import (get_parameters_shaft_diaphragm_panels, plot_shaft_diaphragm_panels)
from src.shaft_secant_piles import check_for_hoop_force
from src.file_utilitites import (st_json_download_button, load_parameters_from_json_file_sdw)#, export_as_pdf)

def main_diaphragm_panel_shaft(st):
    """Main form for diagragm panel shaft

    Args:
        st (streamlit): A streamlit object
    """
    st.title('Geometric and plain concrete resistance check for diaphragm panel shaft')
    st.subheader('(Version 2021.09)')
    # Initial parameters
    parameters = {"project_name_dws": "Sample project", "project_revision_dws": "First issue, rev0", "shaft_name_dws": "Shaft 1", "di_dws": 12.0, "D_dws": 0.8,
                "B_dws": 2.8, "L_dws": 51.3, "v_dws": 0.4, "H_drilling_platform_dws": 0.0, 
                "F_hoop_at_base_dws": 1200.0, "gamma_G_dws": 1.35, "f_ck_dws": 10.0, "alpha_cc_dws": 0.7, "gamma_c_dws": 1.5, 
                "check_more_dws": False, "F_hoop_dws": 1100.0, "L_hoop_dws": 10.0}

    # Load section state
    st.header('Load saved session state (optional)')
    uploaded_file_session_state = st.file_uploader('Select session state file to load', type='json')
    if uploaded_file_session_state is not None:
        try:
            #breakpoint()
            parameters = load_parameters_from_json_file_sdw(uploaded_file_session_state)
            st.success('File successfully loaded')
        except Exception as e:
            st.error(e)

    st.header('Project information')
    project_name = st.text_input('Project', value=parameters['project_name_dws'], key='project_name_dws')
    st.text_input('Revision', value=parameters['project_revision_dws'], key='project_revision_dws')


    st.header('Input parameters')
    col1, col2, col3 = st.columns(3)
    shaft_name = col1.text_input('Shaft identification', value=parameters['shaft_name_dws'], key='shaft_name_dws')
    di = col1.number_input('Shaft inner diameter [m]', value=parameters['di_dws'], format='%.2f', min_value=1.0, max_value=100.0, step=1.0, key='di_dws')
    D = col2.number_input('Pannel thickness [m]', value=parameters['D_dws'], format='%.2f', min_value=0.3, max_value=5.0, step=0.1, key='D_dws')
    B = col3.number_input('Pannel length (for plotting) [m]', value=parameters['B_dws'], format='%.2f', min_value=0.3, max_value=15.0, step=0.1, key='B_dws')
    #n_pieces = int(col3.number_input('Numer of pannels [-]', value=int(parameters['n_pieces_dws']), format='%i', min_value=4, max_value=1000, step=1, key='n_pieces_dws'))
    L = col2.number_input('Length of shaft [m]', value=parameters['L_dws'], step=1.0,min_value=1.0, max_value=150.0, key='L_dws')
    v = col3.number_input('Drilling verticality [%]', value=parameters['v_dws'], step=0.1, min_value=0.05, max_value=2.0, key='v_dws')
    col1, col2 = st.columns(2)
    H_drilling_platform = col1.number_input('Height of drilling platform above top of piles [m]', value=parameters['H_drilling_platform_dws'], step=1.0, min_value=0.0, max_value=20.0, key='H_drilling_platform_dws')
    col2.write('The initial devivation by free drilling x0 = {:.2f} cm'.format(H_drilling_platform*v))

    x0, x, d_eff = get_parameters_shaft_diaphragm_panels(D, L, H_drilling_platform, v)

    st.header('Output parameters for {}'.format(shaft_name))
    col1, col2 = st.columns(2)
    col1.write('Deviation at bottom of shaft dx = {:.2f} cm'.format(x*100))
    col1.write('Effective pannel thickness at bottom of shaft d_eff = {:.2f} cm'.format(d_eff*100))
    if d_eff <= 0:
        col2.warning('PANELS DO NOT TOUCH IN BASE OF SHAFT!!')


    st.header('Visualization for {}'.format(shaft_name))
    fig1 = plot_shaft_diaphragm_panels(di, D, B, x0, x, shaft_name)
    st.pyplot(fig1)


    st.header('Check for hoop stress at base of shaft')
    col1, col2, col3 = st.columns(3)
    F_hoop_at_base = col1.number_input('Hoop force [kN/m]', value=parameters['F_hoop_at_base_dws'], min_value=10.0, max_value=100000.0, step=100.0, key='F_hoop_at_base_dws')
    gamma_G = col2.number_input('gamma_G [-]', value=parameters['gamma_G_dws'], min_value=1.0, max_value=2.0, step=0.05, key='gamma_G_dws')
    f_ck = col3.number_input('f_ck [MPa]', value=parameters['f_ck_dws'], min_value=5.0, max_value=80.0, step=5.0, key='f_ck_dws')
    alpha_cc = col1.number_input('alpha_cc [-]', value=0.7, min_value=0.0, max_value=1.0, step=0.1, key='alpha_cc_dws')
    gamma_c = col2.number_input('gamma_c [-]', value=1.5, min_value=0.0, max_value=2.0, step=0.1, key='gamma_c_dws')
    sigma_cd, f_cd = check_for_hoop_force(F_hoop_at_base, d_eff, gamma_G, f_ck, alpha_cc, gamma_c)
    if sigma_cd < f_cd:
        st.success('Hoop stress = {0:.2f} MPa < design hoop stress = {1:.2f} MPa: PASSED'.format(sigma_cd, f_cd))
    else:
        st.error('Hoop stress = {0:.2f} MPa > design hoop stress = {1:.2f} MPa: NOT PASSED'.format(sigma_cd, f_cd))

    check_more = st.checkbox('Check for hoop stress at any shaft depth', value=parameters['check_more_dws'], key='check_more_dws')
    if check_more:
        #st.header('Check for hoop stress at any shaft depth')
        col1, col2 = st.columns(2)
        F_hoop = col1.number_input('Hoop force [kN/m]', value=parameters['F_hoop_dws'], min_value=10.0, max_value=100000.0, step=100.0, key='F_hoop_dws')
        L_hoop_dws = col2.number_input('Depth from top of shaft [m]', value=parameters['L_hoop_dws'], min_value=1.0, max_value=150.0, step=1.0, key='L_hoop_dws')
        x0, x, d_eff = get_parameters_shaft_diaphragm_panel(D, L_hoop_dws, H_drilling_platform, v)
        sigma_cd, f_cd = check_for_hoop_force(F_hoop, d_eff, gamma_G, f_ck, alpha_cc, gamma_c)
        if sigma_cd < f_cd:
            st.success('Hoop stress = {0:.2f} MPa < design hoop stress = {1:.2f} MPa: PASSED'.format(sigma_cd, f_cd))
        else:
            st.error('Hoop stress = {0:.2f} MPa > design hoop stress = {1:.2f} MPa: NOT PASSED'.format(sigma_cd, f_cd))


    # Save section state
    st.header('Report and save session state')
    #figs = [fig1, fig2]

    button_print_report = st.button('Export PDF', key='export_pdf_sps')
    if button_print_report:
        st.write('Not yet implemented!')
        #export_as_pdf(fig1)

    # Download session state JSON file
    session_state = dict(st.session_state)  # LazySessionState to dict

    download_filename = 'shaft_diaphragm_panels_' + project_name + '.JSON'
    st_json_download_button(session_state, download_filename)