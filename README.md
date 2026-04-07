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

Below are separate instructions for each case:

- [3 Detector search setup](./3DET.md)
- [4 Detector search setup](./4DET.md)

# Plotting

Here I will cover all the plots shown in the paper and how they were created.

[Log Signal-ratio](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/signal_ratio.ipynb): This takes the output of the modified sampler as well as the output of the original histogram sampler (https://github.com/gwastro/pycbc/blob/master/bin/all_sky_search/pycbc_dtphase) and plots the distribution of the signal ratio in both cases.

[Uncertainty correlations](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Uncertainty_Modelling/uncertainties.ipynb): This simulates a bunch of GW signals, performs a matched-filter search and performs statistical tests on the uncertainities measured.

[4det Backgrounds](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Backgrounds.ipynb): This takes some outputs of the 4 det search and plots the backgrounds of all multi-ifo combinations. Memebers of LIGO should be able to run this on the Caltech cluster, otherwise you can reuqest the files and we would be happy to provide as they are too large to include here.

[4det Found/Missed](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Found_missed.ipynb): This takes some outputs of the 4 det search and plots the distributions of found and missed injections. Memebers of LVK should be able to run this on the Caltech cluster, otherwise you can reuqest the files and we would be happy to provide as they are too large to include here.

[File_size](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/File_size.ipynb): This compares the file sizes for the two different methodologies, to run this you will need output files for the two methodologies.

[Appendix Amplitude Distribution](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Appendix_amplitude_dist.ipynb): This just shows the distributions of amplitudes due to our inclusions of distance. No files are required to run this.

[Appendix ML training](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Flow_training.ipynb): This produces corner plots comparing the distribution learned by the flow to the training data. To run this you will need both the smaples the NF was trained on as well as the output file from the ML-training script.

[Cost](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Cost.ipynb): This produces a comparison of the runtimes of the two different methodogies. The times we used from our test can be found here ([Original_2DET](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Timing_results/timing_results_Original_2DET.csv), [Original_3DET](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Timing_results/timing_results_Original_3DET.csv), [FLOW_2DET](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Timing_results/timing_results_Flow_2DET.csv), [FLOW_3DET](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/Timing_results/timing_results_Flow_3DET.csv))

[Recovered Injections](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Plotting/plot_fraction_found_injs.ipynb): The plots the fraction of found injections for each method. This requires the combined HDFINJFIND files from each search, some of these will also need to be recreated for certain detector combinations by rerunning the pycbc_coinc_hdfinjfind jobs but only including the statmap files of that specific detector combination. These files are too large to include here but we are happy to share the ones we used if you request.
