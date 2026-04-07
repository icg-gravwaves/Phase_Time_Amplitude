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

- [HV](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_H1V1_FLOW.h5)
 
- [HL](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_L1H1_FLOW.h5)
 
- [LV](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_L1V1_FLOW.h5)

- [HK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_H1K1_FLOW.h5)
 
- [LK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_L1K1_FLOW.h5)
 
- [VK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_V1K1_FLOW.h5)

- [HLV](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_L1H1V1_FLOW.h5)

- [HLK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_H1L1K1_FLOW.h5)

- [HVK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_H1V1K1_FLOW.h5)

- [LVK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_L1V1K1_FLOW.h5)

- [HLVK](https://github.com/icg-gravwaves/Phase_Time_Amplitude/blob/main/Statistic_Files/4det/PHASE_TIME_AMP_L1H1V1K1_FLOW.h5)

In addition statitsic corrrections are need alongside these to ensure consistent normalization;

HV: -2.200

HL: -1.06228

LV: -2.258

HK: -2.2547

LK: -2.0959

VK: -2.2361

HLV:  -0.6437

HLK: -0.91869

HVK: -1.9396

LVK: -1.19984

HLVK: -1.7987
