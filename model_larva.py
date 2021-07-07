from brian2 import *


def Model(Parameters):

    """ Creates the network model architecture including NeuronGroups, Synapses and initializations.

    Parameters:
        Parameters (dict): collection of cellular parameters and synaptic weights

    Returns:
        NG(dict): NeuronGroups
        c (dict): Synapses

    """


    #ORN
    ORN_eqs = '''
        dv/dt = (g_l*(E_l-v) + g_e*(E_e-v) - g_i*(E_i-v) - g_Ia*(E_Ia-v) + I0)/C_m    : volt (unless refractory) # Ia is the spike triggered adaptation
        dg_e/dt = -g_e/tau_e  : siemens  # post-synaptic exc. conductance # synapses
        dg_i/dt = -g_i/tau_i  : siemens  # post-synaptic inh. conductance
        dg_Ia/dt = -g_Ia/tau_Ia : siemens # conductance adaptation 'current'
        I0 : amp
        '''

    neuron_modelORN = dict()
    neuron_modelORN['model'] = Equations(ORN_eqs, DeltaT=1 * mV, g_l=Parameters['gL'], E_l=Parameters['EL'], E_e=Parameters['Ee'], E_i=Parameters['Ei'], E_Ia=Parameters['EIa'], C_m=Parameters['C'],
    tau_e=Parameters['tau_syn_e'],tau_i=Parameters['tau_syn_i'], tau_Ia=Parameters['tau_Ia'])
    neuron_modelORN['threshold'] = 'v > VT'
    neuron_modelORN['reset'] = '''v = Vr; g_Ia-=ORN_SFA''' 
    neuron_modelORN['refractory'] = Parameters.get('tau_ref')



    #PN
    PN_eqs = '''
        dv/dt = (g_l*(E_l-v) + g_e*(E_e-v) - g_i*(E_i-v) - g_Ia*(E_Ia-v) + I0)/C_m    : volt (unless refractory) # Ia is the spike triggered adaptation
        dg_e/dt = -g_e/tau_e  : siemens  # post-synaptic exc. conductance # synapses
        dg_i/dt = -g_i/tau_i  : siemens  # post-synaptic inh. conductance
        dg_Ia/dt = -g_Ia/tau_Ia : siemens # conductance adaptation 'current'
        I0 : amp
        '''

    neuron_modelPN = dict()
    neuron_modelPN['model'] = Equations(PN_eqs, DeltaT=1 * mV, g_l=Parameters['gLPN'], E_l=Parameters['ELPN'], E_e=Parameters['Ee'], E_i=Parameters['Ei'], E_Ia=Parameters['EIa'],C_m=Parameters['CPN'],
                                        tau_e=Parameters['tau_syn_e'], tau_i=Parameters['tau_syn_i'], tau_Ia=Parameters['tau_Ia'])
    neuron_modelPN['threshold'] = 'v > VTPN'
    neuron_modelPN['reset'] = 'v = VrPN'
    neuron_modelPN['refractory'] = Parameters.get('tau_ref')



    #LN
    LN_eqs = '''
       dv/dt = (g_l*(E_l-v) + g_e*(E_e-v) - g_i*(E_i-v) - g_Ia*(E_Ia-v) + I0)/C_m    : volt (unless refractory) # Ia is the spike triggered adaptation
       dg_e/dt = -g_e/tau_e  : siemens  # post-synaptic exc. conductance # synapses
       dg_i/dt = -g_i/tau_i  : siemens  # post-synaptic inh. conductance
       dg_Ia/dt = -g_Ia/tau_Ia : siemens # conductance adaptation 'current'
       I0 : amp
       '''

    neuron_modelLN = dict()
    neuron_modelLN['model'] = Equations(LN_eqs, DeltaT=1 * mV, g_l=Parameters['gLPN'], E_l=Parameters['ELLN'], E_e=Parameters['Ee'], E_i=Parameters['Ei'], E_Ia=Parameters['EIa'],
                                        C_m=Parameters['CLN'], tau_e=Parameters['tau_syn_e'], tau_i=Parameters['tau_syn_i'], tau_Ia=Parameters['tau_Ia'])
    neuron_modelLN['threshold'] = 'v > VTLN'
    neuron_modelLN['reset'] = 'v = VrLN'
    neuron_modelLN['refractory'] = Parameters.get('tau_ref')




    #KC
    KC_eqs = '''
        dv/dt = (g_l*(E_l-v) + g_e*(E_e-v) - g_i*(E_i-v) - g_Ia*(E_Ia-v) + I0)/C_m    : volt (unless refractory) # Ia is the spike triggered adaptation
        dg_e/dt = -g_e/tau_e  : siemens  # post-synaptic exc. conductance # synapses
        dg_i/dt = -g_i/tau_i  : siemens  # post-synaptic inh. conductance
        dg_Ia/dt = -g_Ia/tau_Ia : siemens # conductance adaptation 'current'
        I0 : amp
        '''

    neuron_modelKC = dict()
    neuron_modelKC['model'] = Equations(KC_eqs, DeltaT=1 * mV, g_l=Parameters['gLKC'], E_l=Parameters['ELKC'], E_e=Parameters['Ee'], E_i=Parameters['Ei'], E_Ia=Parameters['EIa'],
                                        C_m=Parameters['CKC'],tau_e=Parameters['tau_syn_e'], tau_i=Parameters['tau_syn_i'], tau_Ia=Parameters['tau_Ia'])
    neuron_modelKC['threshold'] = 'v > VTKC'
    neuron_modelKC['reset'] = '''v = VrKC; g_Ia-=KC_SFA '''
    neuron_modelKC['refractory'] = Parameters.get('tau_ref')



    # APL
    APL_eqs = '''
        dv/dt = (g_l*(E_l - v) +g_e*(E_e-v)- g_i*(E_i-v))/C_m : volt (unless refractory)
        dg_e/dt = -g_e/tau_e: siemens
        dg_i/dt = -g_i/tau_i : siemens
        '''

    neuron_modelAPL = dict()
    neuron_modelAPL['model'] = Equations(APL_eqs, Delta=1*mV, g_l=Parameters['gL'],E_l=Parameters['EL'],
                                        E_e=Parameters['Ee'],E_i=Parameters['Ei'],C_m=Parameters['CAPL'],tau_e=Parameters['tau_syn_e'],
                                        tau_i=Parameters['tau_syn_i'])
    neuron_modelAPL['threshold'] = 'v > VTAPL'
    neuron_modelAPL['reset'] = '''v = VrAPL'''
    neuron_modelAPL['refractory'] = Parameters['tau_ref']

    # create neuron groups and initialize

    NG = dict()

    NG['ORN'] = NeuronGroup(Parameters.get('N_glo'), **neuron_modelORN, method='euler', namespace=Parameters)
    NG['PN'] = NeuronGroup(Parameters.get('N_glo'), **neuron_modelPN, method='euler', namespace=Parameters)
    NG['LN'] = NeuronGroup(Parameters.get('N_glo'), **neuron_modelLN, method='euler', namespace=Parameters)
    NG['KC'] = NeuronGroup(Parameters.get('N_KC'), **neuron_modelKC, method='euler', namespace=Parameters)
    NG['APL'] = NeuronGroup(1, **neuron_modelAPL, method='euler', namespace=Parameters)


    # initialize voltage at the beginning of the simulation to Vresting

    NG['ORN'].v = Parameters.get('Vr')
    NG['PN'].v = Parameters.get('VrPN')
    NG['LN'].v = Parameters.get('VrLN')
    NG['KC'].v = Parameters.get('VrKC')
    NG['APL'].v = Parameters.get('VrAPL')




    ### synaptic connectivity

    c = dict()

    # connecting input group to ORNs


    c['ORNPN'] = Synapses(NG['ORN'], NG['PN'], 'w : siemens', on_pre='g_e += w')
    for i in np.arange(Parameters.get('N_glo')):
        c['ORNPN'].connect(i=list(range(i * Parameters.get('ORNperGlo'), (i + 1) * Parameters.get('ORNperGlo'))), j=i)
        c['ORNPN'].w = Parameters.get('wORNPN')

    # ORN - LN
    c['ORNLN'] = Synapses(NG['ORN'], NG['LN'], 'w : siemens', on_pre='g_e += w')
    for i in np.arange(Parameters.get('N_glo')):
        c['ORNLN'].connect(i=list(range(i * Parameters.get('ORNperGlo'), (i + 1) * Parameters.get('ORNperGlo'))), j=i)
        c['ORNLN'].w = Parameters.get('wORNLN')

    # LN - PN
    c['LNPN'] = Synapses(NG['LN'], NG['PN'], 'w : siemens', on_pre='g_i -= w')  # inhibitory synapses
    c['LNPN'].connect(p=Parameters['lateral_inhibition_enabled']) # conection probability = 1 or 0 when lateral inhibition
    c['LNPN'].w = Parameters.get('wLNPN')

    # PN - KC
    # one to one connectivity according to Eichler et al. (2017), right hemisphere; rest randomized

    np.random.seed(999)  # fix PN-KC connectivity matrix for comparison with neuromorphic experiments

    connectivity = np.zeros((72, 21))

    # random connections for KCs

    for KC in range(72):
        connections = np.random.randint(2, 6)
        a = np.random.randint(0, 21, size=connections)
        connectivity[KC, a] = 1

    singleKC = np.random.randint(0, 72, size=13)  # single claw KCs

    connectivity[singleKC] = 0

    # deterministic one to one connections
    connectivity[singleKC[0], 0] = 1
    connectivity[singleKC[1], 1] = 1
    connectivity[singleKC[2], 4] = 1
    connectivity[singleKC[3], 6] = 1
    connectivity[singleKC[4], 7] = 1
    connectivity[singleKC[5], 8] = 1
    connectivity[singleKC[6], 9] = 1
    connectivity[singleKC[7], 11] = 1
    connectivity[singleKC[8], 13] = 1
    connectivity[singleKC[9], 14] = 1
    connectivity[singleKC[10], 16] = 1
    connectivity[singleKC[11], 19] = 1
    connectivity[singleKC[12], 20] = 1

   
   
    targets, sources = connectivity.nonzero()  

    np.random.seed(seed=None)

    c['KC'] = Synapses(NG['PN'], NG['KC'], 'w : siemens', on_pre='g_e += w')
    c['KC'].connect(i=sources, j=targets)  

    # connectivity matrix
    c['KC'].w = Parameters.get('wPNKC')

    # KC-APL
    c['KCAPL'] = Synapses(NG['KC'], NG['APL'], 'w:siemens', on_pre='g_e+=w', delay=Parameters['delay_KCAPL'])
    c['KCAPL'].connect(i=[31, 15, 17, 3, 33, 70, 8, 48, 2, 63, 2, 55, 22, 18, 20, 9, 66, 58, 19, 21, 71, 32, 0, 41, 56, 62, 50, 4, 67,
           12, 37, 13, 54, 49, 26, 65, 64, 24, 52, 23, 40, 10, 25, 45, 27, 42, 44, 5, 69, 46, 1, 59, 30, 53, 11, 57, 36,
           43, 16, 61, 68, 39, 51, 14], j=0)
    c['KCAPL'].w = Parameters['wKCAPL']


    # APL-KC
    c['APLKC'] = Synapses(NG['APL'], NG['KC'], 'w:siemens', on_pre='g_i -= w', delay=Parameters['delay_APLKC'])
    c['APLKC'].connect(p=Parameters['APL_inhibition'])
    c['APLKC'].w = Parameters['wAPLKC']


    return NG,c


