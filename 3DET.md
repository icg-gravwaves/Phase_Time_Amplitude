# 3 Detector

The workflow can be submitted through using The workflow can be submitted through using `pycbc_make_offline_search_workflow`. See [Here](https://pycbc.org/pycbc/latest/html/workflow/pycbc_make_offline_search_workflow.html) for more information on how to run this.

This requires the following config files;

[data_O4_HLV_C00_AR.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/data_O4_HLV_C00_AR.ini)

[gps_times_chunk35.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/gps_times_chunk35.ini)

[injections_chunk35.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/injections_chunk35.ini)

[analysis.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/analysis.ini)

[analysis_HLV.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/analysis_HLV.ini)

[executable_common.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/executables_common.ini)

[injections_common.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/injections_common.ini)

[inspiral.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/inspiral.ini)

[plotting.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/plotting.ini)

A lot of these are also set up to use LIGO resources, so in their current form will only be able to be run by those who are a memeber of LIGO. These data are the same as those available from GWOSC, but the PyCBC tools may need some changes to use GWOSC to access them. The reader may find [4-OGC: Catalog of gravitational waves from compact-binary mergers](https://github.com/gwastro/4-ogc) helpful if neeeding to make these changes.

You will need to change the statistic files in the analysis.ini and analysis_HLVK.ini files when rerunning for the statistic adjustments. The stat files we generated and used in the searches presented in the paper are;

Modified;

- [HV](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/HV_Samples_Mod.hdf)

- [HL](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/LH_Samples_Mod.hdf)

- [LV](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/LV_Samples_Mod.hdf)

Normalizing Flow;

- [HV](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/PHASE_TIME_AMP_H1V1_FLOW.h5)

- [HL](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/PHASE_TIME_AMP_L1H1_FLOW.h5)

- [LV](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/PHASE_TIME_AMP_L1V1_FLOW.h5)

- [HLV](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/PHASE_TIME_AMP_L1H1V1_FLOW.h5)

In addition statitsic corrrections are need alongside these to ensure consistent normalization.

Modified;

HV: -1.368

HL: -0.659

LV: -1.275

Normlaizing Flow;

HV: -1.60

HL: -0.997

LV: -1.399

HLV:  -1.17
