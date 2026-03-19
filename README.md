# Normalizing Flows for Density Estimation in Multi-Detector Gravitational-Wave Searches

This is the data release for the paper "Normalizing Flows for Density Estimation in Multi-Detector Gravitational-Wave Searches". In this paper we have demonstrated the use of a machine learning approach to density estimation, called normalizing flows as an alternative to histogram-based estimators used with PyCBC searches for compact binary coalescences. We release the code used to produce both the results and plots found in the paper.

# Sampling

In this project we relaxed  a number of simplifying assumptions in the current Monte-Carlo sampling of simulated signals. The resulting sampler incorporating these changes can be found here: 

[Modified Sampler](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Sampling/PTA_sampling_MODIFIED.py)

This was used to produce the MODIFIED data set presented in the paper. For the search we ran with these samples, our histogram files contained approximately 1,000,000 samples.

---

A number of additional changes were included for these samples to then train a normalizing flow. The resulting sampler file incorporating these can be found here:

[Flow Sampler](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Sampling/PTA_samples.py)

This was used to produce the FLOW data set presented in the paper. For 2 and 3 detector cases we found 500,000 samples were sufficient for training the normalizing flow.

---

For a particular distribution you will need to give arguments defining the ifos and relative sensitivities. In this paper, for three detctor searches we used the following relative sensitivities, 1.0, 0.94 and 0.32 for L1, H1 and V1 respectively. 

# Normalizing Flow

For the FLOW data set the samples generated then need to be used to train the normalizing flow model. This can be done using the following file:

[Normalizing Flow Trainer](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Normalizing_Flow/ML_training.py)

With this requiring the output file from the sampler as its only argument. An additional stat file is required to run this which can be found here:

[Normalizing Flow Stat File](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Normalizing_Flow/ml_stat.py)
