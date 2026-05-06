# 3 Detector

# Work in Progress

<!--

[data_O4_HLV_C00_AR.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/data_O4_HLV_C00_AR.ini)

[gps_times_chunk35.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/gps_times_chunk35.ini)

[injections_chunk35.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/injections_chunk35.ini)

In addition, for the statistic adjustment reruns you will need to downlaoded and edit the following files, replacing the statistic files with the ones generated using the method above. 

[analysis.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/analysis.ini)

[analysis_HLV.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/3DET/analysis_HLV.ini)

-->

The stat files we generated and used in the searches presented in the paper are;

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
