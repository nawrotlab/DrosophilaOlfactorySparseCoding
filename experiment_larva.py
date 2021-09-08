from brian2 import *
from model_larva import Model
import numpy as np
from AttrDict import AttrDict
from stimulus import gamma
from joblib import Parallel, delayed
from elephant.spike_train_generation import homogeneous_gamma_process
from quantities import Hz as qHz
from quantities import  ms as qms


safe = True
save_path = "path"




Parameters = dict(

    # sparseness mechanisms
    lateral_inhibition_enabled=1, # 0 or 1
    APL_inhibition= 0,  # 0 or 1
    KC_SFA=0.05* nS, # conductance adaptation
    ORN_SFA= 0.1 * nS, # conductance adaptation

    # Neuron Parameters
    C=100 * pF,   # capacitance 
    CMBON = 100*pF, # capacitance MBON 
    CKC=30 * pF, # capacitance KC
    CPN=30 * pF, # capacitance PN
    CLN=30 *pF,# capacitance LN
    CAPL=200 * pF, # capacitance APL
   
    gL=5 * nS, # leak conductance 
    gLKC=0.5 * nS, # leak conductance KC
    gLPN=2.5 * nS, # leak conductance PN
    EL=-60 * mV, # leak potential
    ELPN=-59 * mV, # leak potential PN
    ELLN=-59 * mV,  # leak potential LN
    ELKC=-55 * mV,  # leak potential KC
    
    VT=-35 * mV, # spike threshold 
    VTPN=-30 * mV, # spike threshold PN
    VTLN=-30 * mV,  # spike threshold LN
    VTKC=-35 * mV,  # spike threshold KC
    VTAPL=-30 * mV,  # spike threshold APL
    Vr=-60 * mV, # resting potential
    VrPN=-59 * mV,  # resting potential PN
    VrLN=-59 * mV,  # resting potential LN
    VrKC=-55 * mV, # resting potential KC
    VrAPL=-60 * mV, # resting potential APL

    tau_ref=2 * ms, # refractory time 
    delay_KCAPL=0 * ms, # synaptic delay
    delay_APLKC=0 * ms,
  

    # Dimensions
    N_glo=21,
    ORNperGlo=1,
    N_KC=72,
   

    # Synaptic Parameters
    Ee=0 * mV, # excitatory synaptic potential
    Ei=-75 * mV,  # inhibitory synaptic potential
    tau_syn_e=5 * ms, # excitatory synaptic time constant
    tau_syn_i=10 * ms, # inhibitory synaptic time constant

    # # weights 
    wORNinputORN=3 * nS, wORNPN=30 * nS, wORNLN=9 * nS,
    wLNPN=2 * nS,  wPNKC=1 * nS, wKCAPL=50 * nS, wAPLKC=100 * nS,

    # Adptation current Parameters
    tau_Ia = 1000*ms, 
    EIa = -90*mV, 

    # simulation
    dt = 0.1*ms)






def experiment(Parameters,filename):

    # set up model architecture
    NG,c = Model(Parameters)

    # create input stimulus (odor)
    odor_pattern = gamma()


    spike_times = []
    spike_index = []

    for neuron, value in enumerate(odor_pattern):
        spikes = homogeneous_gamma_process(10.0, (250* 10.0) * qHz, 0 * qms, 6000 * qms,as_array=True)  # spontaneous activity
        for elem in spikes:
            spike_times.append(elem)
            spike_index.append(neuron)
        spikes = homogeneous_gamma_process(10.0, (value * 10.0) * qHz, 2000 * qms, 4000 * qms,as_array=True) #value
        for elem in spikes:
            spike_times.append(elem)
            spike_index.append(neuron)

    # input to SpikeGeneratorGroup is cleaned up to remove multiple spikes of one neuron during a dt
    spike_index = np.array(spike_index)
    spike_times = np.array(spike_times)
    spike_times = np.around(spike_times,decimals=1) 


    temp_index = []
    temp_times = []
    for i, elem in enumerate(np.unique(spike_index)):
        spike_times_temp = spike_times[spike_index == elem]
        clean_spike_times = np.unique(spike_times_temp, return_index=True)[0]
        temp_times.extend(clean_spike_times)
        [temp_index.append(elem) for x in clean_spike_times]

    spike_times = temp_times
    spike_index = temp_index

    # input activation of ORNs
    NG['ORNinput'] = SpikeGeneratorGroup(Parameters['N_glo'], spike_index, spike_times * ms)
    input = SpikeMonitor(NG['ORNinput'])

    # ORNinput- ORN synapse

    c['ORNinputORN'] = Synapses(NG['ORNinput'], NG['ORN'], 'w : siemens', on_pre='g_e+=w')
    for i in np.arange(Parameters.get('N_glo')):
        c['ORNinputORN'].connect(i=list(range(i * Parameters.get('ORNperGlo'), (i + 1) * Parameters.get('ORNperGlo'))), j=i)
        c['ORNinputORN'].w = Parameters.get('wORNinputORN')



    # monitors

    spikemonitors = dict()

    spikemonitors['spikeORN'] = SpikeMonitor(NG['ORN'])
    spikemonitors['spikePN'] = SpikeMonitor(NG['PN'])
    spikemonitors['spikeLN'] = SpikeMonitor(NG['LN'])
    spikemonitors['spikeKC'] = SpikeMonitor(NG['KC'])
    spikemonitors['spikeAPL'] = SpikeMonitor(NG['APL'])




    # setup network

    net = Network(NG.values(),c.values())

    net.add(spikemonitors)


    # Running the simulation
    ParaWithLocals = dict()
    ParaWithLocals.update(Parameters)
    ParaWithLocals.update(locals())

    net.run(6000 * ms, namespace=ParaWithLocals)

    if safe:


        spikemons = dict()

        spikemons['spikeORN'] = AttrDict({'i': spikemonitors['spikeORN'].i[:],
                                         't': spikemonitors['spikeORN'].t[:]})
        spikemons['spikePN'] = AttrDict({'i': spikemonitors['spikePN'].i[:],
                                          't': spikemonitors['spikePN'].t[:]})
        spikemons['spikeLN'] = AttrDict({'i': spikemonitors['spikeLN'].i[:],
                                          't': spikemonitors['spikeLN'].t[:]})
        spikemons['spikeKC'] = AttrDict({'i': spikemonitors['spikeKC'].i[:],
                                          't': spikemonitors['spikeKC'].t[:]})
        spikemons['spikeAPL'] = AttrDict({'i': spikemonitors['spikeAPL'].i[:],
                                           't': spikemonitors['spikeAPL'].t[:]})

        spikemons = AttrDict(spikemons)


        data = {'spikemons': spikemons,
                'Parameters': Parameters,
                }



        d = AttrDict(data)

        np.savez(os.path.join(save_path,filename), data=d)


     


##### data collection #####

sample = np.arange(1)

Parallel(n_jobs=len(sample))(delayed(experiment)(Parameters=Parameters, filename=f"Larva_{animal:02}")for animal in sample)









