# 4 Detector

The workflow can be submitted through using this following script

[run.sh](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/run.sh)

This requires the following config files;

[data_O4_HLVK_C00_AR.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/data_O4_HLVK_C00_AR.ini)

[gps_times_chunk18.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/gps_times_chunk18.ini)

[minimal_injections.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/minimal_injections.ini)

[executables_common.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/executables_common.ini)

[executables_for_scitokens.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/executables_for_scitokens.ini)

[executables_osg.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/executables_osg.ini)

[inspiral.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/inspiral.ini)

[plotting.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/plotting.ini)

[reuse_banks.cache](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/reuse_banks.cache)

[DQ-dummy-file.xml](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/DQ-dummy-file.xml)

[VDF.xml](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/VDF.xml)

[analysis.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/analysis.ini)

[analysis_HLVK.ini](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Configs/4DET/analysis_HLVK.ini)

Similarly to the 3 detector case, you will need to change the statistic files in the analysis.ini and analysis_HLVK.ini files when rerunning for the statistic adjustments.

The files we generated and used in the searches presented in the paper are;

- [HV](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/PHASE_TIME_AMP_H1V1_FLOW.h5)
 
- [HL](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/PHASE_TIME_AMP_L1H1_FLOW.h5)
 
- [LV](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/PHASE_TIME_AMP_L1V1_FLOW.h5)

- [HK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/PHASE_TIME_AMP_H1V1_FLOW.h5)
 
- [LK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/PHASE_TIME_AMP_L1H1_FLOW.h5)
 
- [VK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/PHASE_TIME_AMP_L1V1_FLOW.h5)

- [HLV](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/PHASE_TIME_AMP_L1H1V1_FLOW.h5)

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
