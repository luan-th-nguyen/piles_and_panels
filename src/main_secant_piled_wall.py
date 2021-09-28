import numpy as np
from src.wall_secant_piles import (get_parameters_wall_secant_piles, plot_wall_secant_piles,
                                   plot_wall_secant_piles_3d, plot_wall_secant_piles_2items,
                                   plot_wall_secant_piles_3d_2items)

# Initial parameters
parameters_init = {"project_name_spw": "Sample project", "project_revision_spw": "First issue, rev0", "wall_name_spw": "Wall 1", "D_spw": 1.2,
            "n_pieces_spw": 10, "a_spw": 0.75, "L_spw": 25.0, "v_spw": 0.75, "H_drilling_platform_spw": 0.0, "plotting_option_spw":'Two piles apart'}

def main_secant_piled_wall(st, parameters=None):
    """ Main program for secant piled wall
    """
    if parameters is None:
        parameters = parameters_init

    st.title('Geometric check for secant piled wall')

    st.header('Project information')
    project_name = st.text_input('Project', value=parameters['project_name_spw'], key='project_name_spw')
    st.text_input('Revision', value=parameters['project_revision_spw'], key='project_revision_spw')

    st.header('Input parameters')
    col1, col2, col3 = st.columns(3)
    wall_name = col1.text_input('Wall identification', value=parameters['wall_name_spw'], key='wall_name_spw')
    D = col2.number_input('Pile diameter [m]', value=parameters['D_spw'], format='%.2f', min_value=0.3, max_value=5.0, step=0.1, key='D_spw')
    a = col3.number_input('C/C pile spacing b/w two neighboring piles [m]', value=parameters['a_spw'], format='%.2f', min_value=0.3, max_value=5.0, step=0.1, key='a_spw')
    L = col1.number_input('Length of shaft [m]', value=parameters['L_spw'], step=1.0, min_value=1.0, max_value=150.0, key='L_spw')
    v = col2.number_input('Drilling verticality [%]', value=parameters['v_spw'], step=0.1, min_value=0.05, max_value=2.0, key='v_spw')
    H_drilling_platform = st.number_input('Height of drilling platform above top of piles [m]', value=parameters['H_drilling_platform_spw'], step=1.0, min_value=0.0, max_value=20.0, key='H_drilling_platform_spw')
    st.write('The initial devivation by free drilling x0 = {:.2f} cm'.format(H_drilling_platform*v))
    t_top, d_top, x0, x, t_eff, d_eff = get_parameters_wall_secant_piles(D, a, L, H_drilling_platform, v)

    st.header('Output parameters for {}'.format(wall_name))
    col1, col2 = st.columns(2)
    #col1.write('C/c spacing at top of wall a = {:.2f} m'.format(a))
    col1.write('Overcut at top of wall t = {:.2f} cm'.format(t_top*100))
    col1.write('Effective thickness at top of wall d = {:.2f} cm'.format(d_top*100))
    col1.write('Deviation at bottom of wall dx = {:.2f} cm'.format(x*100))

    if t_eff > 0:
        d_eff = 2*np.sqrt((D/2)*t_eff - (t_eff/2)**2) # overlapped thickness, m    
        col2.write('Overcut at bottom of wall t_eff = {:.2f} cm'.format(t_eff*100))
        col2.write('Effective thickness at bottom of wall d_eff = {:.2f} cm'.format(d_eff*100))
    else:
        d_eff = np.nan
        col2.warning('PILES DO NOT TOUCH IN BASE OF WALL!!')


    st.header('Visualization for {}'.format(wall_name))
    col1, col2 = st.columns(2)
    plotting_options = ['Two piles apart', 'Random deviations']
    plotting_option = col1.selectbox('Type of visualization', plotting_options, index=plotting_options.index(parameters['plotting_option_spw']), key='plotting_option_spw')
    if plotting_option == 'Two piles apart':
        fig1 = plot_wall_secant_piles_2items(a, D, x0, x, wall_name)
        st.pyplot(fig1)
        fig2 = plot_wall_secant_piles_3d_2items(2, a, D, L, x0, x, wall_name)
        st.pyplot(fig2)
    else:
        n_pieces = int(col2.number_input('Number of piles to plot', value=int(parameters['n_pieces_spw']), format='%i', min_value=2, max_value=100, step=1, key='n_pieces_spw'))
        fig1 = plot_wall_secant_piles(n_pieces, a, D, x0, x, wall_name)
        st.pyplot(fig1)
        fig2 = plot_wall_secant_piles_3d(n_pieces, a, D, L, x0, x, wall_name)
        st.pyplot(fig2)
