# Normalizing Flows for Density Estimation in Multi-Detector Gravitational-Wave Searches

This is the data release for the paper "Normalizing Flows for Density Estimation in Multi-Detector Gravitational-Wave Searches". In this paper we have demonstrated the use of a machine learning approach to density estimation, called normalizing flows as an alternative to histogram-based estimators used within PyCBC searches for compact binary coalescences. We release the code used to produce both the results and plots found in the paper.

# Sampling

In this project we relaxed  a number of simplifying assumptions in the current Monte-Carlo sampling of simulated signals. The resulting sampler incorporating these changes can be found here: 

[Modified Sampler](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Sampling/PTA_sampling_MODIFIED.py)

This was used to produce the MODIFIED data set presented in the paper. For the search we ran, we required a sample size of 100,000,000. This may be better off run on 100 separate jobs then combing the resulting hdf files.

---

A number of additional changes were included for these samples to then train a normalizing flow. The resulting sampler file incorporating these can be found here:

[Flow Sampler](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Sampling/PTA_samples.py)

This was used to produce the FLOW data set presented in the paper. For 2 and 3 detector cases we found 500,000 samples were sufficient for training the normalizing flow.

---

For a particular distribution you will need to give arguments defining the ifos and relative sensitivities. In this paper, for three detctor searches we used the following relative sensitivities, 1.0, 0.94 and 0.32 for L1, H1 and V1 respectively. All other arguments used are consistent with their default values. 

# Normalizing Flow

For the FLOW data set the samples generated then need to be used to train the normalizing flow model. This can be done using the following file:

[Normalizing Flow Trainer](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Normalizing_Flow/ML_training.py)

With this requiring the output file from the sampler as its only argument. An additional stat file is required to run this which can be found here:

[Normalizing Flow Stat File](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Normalizing_Flow/ml_stat.py)

# Searches

All searches were run on the Caltech cluster as part of the LIGO data grid, these have substantial computing requirements and would not be able to be run on a laptop. A full initial search was performed on the data chunks to get the "ORIGINAL" results, this was done using the PyCBC 2.3.14 release branch. Once this is completed you can then rerun the backend of the search with the statistic adjustments made during this paper, for this you will want to make sure you reuse all the "INSPIRAL" outputs, as these take a considerable time to run. For this step, we used modified PyCBC branches which can be found here;

Modified run: https://github.com/SamInsley/pycbc/tree/Modified
Normalizing Flow run: https://github.com/SamInsley/pycbc/tree/PTA

We aim to merge a version of this into the main PyCBC branch which will allow you to choose between the histogram-based and Normalizing Flow methodologies.

Below I will go through the configurations used to run both the 3 and 4 detector cases.

---

# 3 Detector


