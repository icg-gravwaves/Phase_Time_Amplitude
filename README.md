# Normalizing Flows for Density Estimation in Multi-Detector Gravitational-Wave Searches

This is the data release for the paper "Normalizing Flows for Density Estimation in Multi-Detector Gravitational-Wave Searches". In this paper we have demonstrated the use of a machine learning approach to density estimation, called normalizing flows as an alternative to histogram-based estimators used with PyCBC searches for compact binary coalescences. We release the code used to produce both the results and plots found in the paper.

# Sampling

In this project we relaxed  a number of simplifying assumptions in the current Monte-Carlo sampling of simulated signals. The resulting sampler incorporating these changes can be found here: 
https://icg-gravwaves.github.io/Phase_Time_Amplitude/Sampling/PTA_sampling_MODIFIED.py.
This was used to produce the MODIFIED data set presented in the paper.

A number of additional changes were included for these samples to then train a normalzing flow. The resulting sampler file incorporating these can be found here:
https://icg-gravwaves.github.io/Phase_Time_Amplitude/Sampling/PTA_samples.py.
This was used to produce the FLOW data set presented in the paper.

For the three-detector analyses presented in the paper, relative sensitivities of 1.0, 0.94 and 0.32 were used for L1, H1 and V1 respectively.

# Normalizing Flow

For the FLOW data set the samples generated then need to be used to train the normalzing flow model. This can be done using the following file:
https://icg-gravwaves.github.io/Phase_Time_Amplitude/Normalizing_Flow/ML_training.py
With this only requiring the output file from the sampler as its only argument. An additional statistic file is required to run this which can be found here:
https://icg-gravwaves.github.io/Phase_Time_Amplitude/Normalizing_Flow/ml_stat.py
