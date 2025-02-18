# General modelling parameters

panel_thickness = 0.012                 # m - panel thickness
sub_layers = 10                         # number of sub layers
delta_x = panel_thickness / sub_layers  # m - thickness of modelled sublayer in wooden panels
D_w_s = 3.0 * 10**(-10)                 # m^2/s - diffusion coefficient of water in wood
D_W_a = 2.5 * 10**(-5)                 # m^2/s - diffusion coefficient of water in air at 22'C
delta_t = 720                           # seconds - modelling timestep (constant)
boundary_layer = 0.01                   # m - boundary layer at wooden wall surface (constant)
gas_constant = 8.314                    # J/(Kg * K) Universal gas constant
mol_weight = 0.018015                   # Kg/mol - molecular weight of water vapor (constant)
fourier = 0.15                          # Fourier number




# Model specific parameters (generic wooden home enclosure describing a combined living room and kitchen)

T_k_in = 295.15         # K - indoor temperature (constant)
T_c_in = 22             # 'C - indoor temperature (constant)
RH_in = 0.35            # initial estimate/guess (variable)
A_ex = 60               # m^2 - wooden area exchanging humidity with the enclosure (constant)
Vol = 120               # m^2 - volume of enclosure (constant)
A_V_Ratio = A_ex/Vol    # ratio of wooden panel exchange area to enclosure volume (constant)
supply_24h = 1          # Kg/24 hour - supplied water vapor from cooking, respiring, plants++
rho_wood = 500          # kg/m^3 - density of wood (constant)
gamma = 380             # Ventilation constant

