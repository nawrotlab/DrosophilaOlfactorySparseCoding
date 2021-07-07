import numpy as np

### creates different stimuli to be used for stimulation of the larval network



def gamma():

    gamma_baseline = 0.000000001  # because elephant.homogenous_gamma() won't take 0 as a rate parameter
    # creating inputs to ORNs

    stim1 = np.array([0, 0, 74, 129, 150, 129, 74, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    stim1 = stim1*4
    stim1 = stim1+gamma_baseline

    stim2 = np.array([0, 0, 0, 0, 0, 74, 129, 150, 129, 74, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    stim2 = stim2 * 4
    stim2 = stim2+gamma_baseline

    stim3 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 74, 129, 150, 129, 74, 0, 0, 0, 0, 0, 0, 0, 0])
    stim3 = stim3*4
    stim3 = stim3+gamma_baseline


    return stim3, stim2, stim3

