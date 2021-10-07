import numpy as np
from src.shaft_secant_piles import (get_parameters_shaft_secant_piles, plot_shaft, 
                                    plot_shaft_3d, check_for_hoop_force, get_area_moment_of_inertia_rect)

# Initial parameters
parameters_init = {"project_name": "Sample project", "project_revision": "First issue, rev0", "shaft_name": "Shaft 1", "di": 12.0, "D": 1.2,
            "n_pieces": 44, "L": 15.0, "v": 0.75, "H_drilling_platform": 0.0, "E": 30.e6,
            "F_hoop_at_base": 700.0, "gamma_G": 1.35, "f_ck": 10.0, "alpha_cc": 0.7, "gamma_c": 1.5, 
            "check_more": False, "F_hoop": 500.0, "L_hoop": 10.0}

def main_secant_piled_shaft(st, parameters=None):
    """ Main program for secant piled shaft
    """
    if parameters is None:
        parameters = parameters_init

    st.title('Geometric and plain concrete resistance check for secant piled shaft')

    st.header('Project information')
    project_name = st.text_input('Project', value=parameters['project_name'], key='project_name')
    st.text_input('Revision', value=parameters['project_revision'], key='project_revision')

    st.header('Input parameters')
    col1, col2, col3 = st.columns(3)
    shaft_name = col1.text_input('Shaft identification', value=parameters['shaft_name'], key='shaft_name')
    di = col1.number_input('Shaft inner diameter [m]', value=parameters['di'], format='%.2f', min_value=1.0, max_value=100.0, step=1.0, key='di')
    D = col2.number_input('Pile diameter [m]', value=parameters['D'], format='%.2f', min_value=0.3, max_value=5.0, step=0.1, key='D')
    n_pieces = int(col3.number_input('Numer of piles [-]', value=int(parameters['n_pieces']), format='%i', min_value=4, max_value=1000, step=1, key='n_pieces'))
    L = col2.number_input('Length of shaft [m]', value=parameters['L'], step=1.0,min_value=1.0, max_value=150.0, key='L')
    v = col3.number_input('Drilling verticality [%]', value=parameters['v'], step=0.1, min_value=0.05, max_value=2.0, key='v')
    col1, col2 = st.columns(2)
    H_drilling_platform = col1.number_input('Height of drilling platform above top of piles [m]', value=parameters['H_drilling_platform'], step=1.0, min_value=0.0, max_value=50.0, key='H_drilling_platform')
    col2.write('The initial devivation by free drilling x0 = {:.2f} cm'.format(H_drilling_platform*v))
    a, t_top, d_top, x0, x, t_eff, d_eff = get_parameters_shaft_secant_piles(di/2, n_pieces, D, L, H_drilling_platform, v, shaft_name=shaft_name, print_results=False)


    st.header('Output parameters for {}'.format(shaft_name))
    col1, col2 = st.columns(2)
    #print('\nOUTPUT GEOMETRY {0}...'.format(shaft_name))
    col1.write('C/c spacing at top of shaft a = {:.2f} m'.format(a))
    col1.write('Overcut at top of shaft t = {:.2f} cm'.format(t_top*100))
    col1.write('Effective thickness at top of shaft d = {:.2f} cm'.format(d_top*100))
    col1.write('Deviation at bottom of shaft dx = {:.2f} cm'.format(x*100))

    if t_eff > 0:
        d_eff = 2*np.sqrt((D/2)*t_eff - (t_eff/2)**2) # overlapped thickness, m    
        col2.write('Overcut at bottom of shaft t_eff = {:.2f} cm'.format(t_eff*100))
        col2.write('Effective thickness at bottom of shaft d_eff = {:.2f} cm'.format(d_eff*100))
        with st.expander('Axial and flexural rigidity considering effective thickness at top and bottom of shaft'):
            E = st.number_input("Concrete Young's modulus E [KPa]", value=parameters['E'], format='%.0f', min_value=25.0e6, max_value=35.0e6, step=1.0E6, key='E')
            display_shaft_stiffnesses(d_top, d_eff, E, st)
    else:
        d_eff = np.nan
        col2.warning('PILES DO NOT TOUCH IN BASE OF SHAFT!!')


    st.header('Visualization for {}'.format(shaft_name))
    fig1 = plot_shaft(di/2, n_pieces, D, x0, x, shaft_name)
    st.pyplot(fig1)
    fig2 = plot_shaft_3d(di/2, n_pieces, D, L, x0, x, shaft_name)
    st.pyplot(fig2)


    st.header('Check for hoop stress at base of shaft')
    col1, col2, col3 = st.columns(3)
    F_hoop_at_base = col1.number_input('Hoop force [kN/m]', value=parameters['F_hoop_at_base'], min_value=10.0, max_value=100000.0, step=100.0, key='F_hoop_at_base')
    gamma_G = col2.number_input('gamma_G [-]', value=parameters['gamma_G'], min_value=1.0, max_value=2.0, step=0.05, key='gamma_G')
    f_ck = col3.number_input('f_ck [MPa]', value=parameters['f_ck'], min_value=5.0, max_value=80.0, step=5.0, key='f_ck')
    alpha_cc = col1.number_input('alpha_cc [-]', value=0.7, min_value=0.0, max_value=1.0, step=0.1, key='alpha_cc')
    gamma_c = col2.number_input('gamma_c [-]', value=1.5, min_value=0.0, max_value=2.0, step=0.1, key='gamma_c')
    sigma_cd, f_cd = check_for_hoop_force(F_hoop_at_base, d_eff, gamma_G, f_ck, alpha_cc, gamma_c)
    if sigma_cd < f_cd:
        st.success('Hoop stress = {0:.2f} MPa < design hoop stress = {1:.2f} MPa: PASSED'.format(sigma_cd, f_cd))
    else:
        st.error('Hoop stress = {0:.2f} MPa > design hoop stress = {1:.2f} MPa: NOT PASSED'.format(sigma_cd, f_cd))


    check_more = st.checkbox('Check for hoop stress at any shaft depth', value=parameters['check_more'], key='check_more')
    if check_more:
        #st.header('Check for hoop stress at any shaft depth')
        col1, col2 = st.columns(2)
        F_hoop = col1.number_input('Hoop force [kN/m]', value=parameters['F_hoop'], min_value=10.0, max_value=100000.0, step=100.0, key='F_hoop')
        L_hoop = col2.number_input('Depth from top of shaft [m]', value=parameters['L_hoop'], min_value=1.0, max_value=150.0, step=1.0, key='L_hoop')
        a, t_top, d_top, x0, x, t_eff, d_eff = get_parameters_shaft_secant_piles(di/2, n_pieces, D, L_hoop, H_drilling_platform, v, shaft_name=shaft_name, print_results=False)
        sigma_cd, f_cd = check_for_hoop_force(F_hoop, d_eff, gamma_G, f_ck, alpha_cc, gamma_c)
        if sigma_cd < f_cd:
            st.success('Hoop stress = {0:.2f} MPa < design hoop stress = {1:.2f} MPa: PASSED'.format(sigma_cd, f_cd))
        else:
            st.error('Hoop stress = {0:.2f} MPa > design hoop stress = {1:.2f} MPa: NOT PASSED'.format(sigma_cd, f_cd))

def display_shaft_stiffnesses(d_top, d_eff, E, st):
    """ Displays shaft stiffness
    """
    I = get_area_moment_of_inertia_rect(1.0, d_top)
    EI = E*I        # [kNm**2/m]
    EA = E*d_top    # [kN/m]
    st.write('EI at top = {0:.2f} [kNm^2/m], EA at top = {1:.2f} [kN/m]'.format(EI, EA))
    I = get_area_moment_of_inertia_rect(1.0, d_eff)
    EI = E*I        # [kNm**2/m]
    EA = E*d_eff    # [kN/m]
    st.write('EI at bottom = {0:.2f} [kNm^2/m], EA at bottom = {1:.2f} [kN/m]'.format(EI, EA))
