# 4 Detector

The workflow can be submitted through using The workflow can be submitted through using `pycbc_make_offline_search_workflow`. See [Here](https://pycbc.org/pycbc/latest/html/workflow/pycbc_make_offline_search_workflow.html) for more information on how to run this.

This requires the following config files;

[data_O4_HLVK_C00_AR.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/data_O4_HLVK_C00_AR.ini)

[gps_times_chunk18.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/gps_times_chunk18.ini)

[minimal_injections.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/minimal_injections.ini)

[executables_common.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/executables_common.ini)

[executables_for_scitokens.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/executables_for_scitokens.ini)

[executables_osg.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/executables_osg.ini)

[inspiral.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/inspiral.ini)

[plotting.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/plotting.ini)

[analysis.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/analysis.ini)

[analysis_HLVK.ini](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/analysis_HLVK.ini)


In addition there are several sections that point to files the user may not be able to access such as `[workflow-segments-k1]`. These files can be downloaded here then you will need to change the configuration file to redirect to them.

[VDF.xml](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/VDF.xml)

[DQ-dummy-file.xml](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/DQ-dummy-file.xml)

[k1-science.xml](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/extra-stuff/k1_science.xml)

[k1-segments.xml](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/extra-stuff/k1_segments.xml)

[k1-vetoes.xml](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Configs/4DET/extra-stuff/k1_vetoes.xml)

A lot of these are also set up to use LIGO resources, so in their current form will only be able to be run by those who are a memeber of LIGO. These data are the same as those available from GWOSC, but the PyCBC tools may need some changes to use GWOSC to access them. The reader may find [4-OGC: Catalog of gravitational waves from compact-binary mergers](https://github.com/gwastro/4-ogc) helpful if neeeding to make these changes.

Similarly to the 3 detector case, you will need to change the statistic files in the analysis.ini and analysis_HLVK.ini files when rerunning for the statistic adjustments.

The files we generated and used in the searches presented in the paper are;

- [HV](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_H1V1_FLOW.h5)

- [HL](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_L1H1_FLOW.h5)

- [LV](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_L1V1_FLOW.h5)

- [HK](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_H1K1_FLOW.h5)

- [LK](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_L1K1_FLOW.h5)

- [VK](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_V1K1_FLOW.h5)

- [HLV](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_L1H1V1_FLOW.h5)

- [HLK](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_H1L1K1_FLOW.h5)

- [HVK](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_H1V1K1_FLOW.h5)

- [LVK](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_L1V1K1_FLOW.h5)

- [HLVK](https://raw.githubusercontent.com/icg-gravwaves/Phase_Time_Amplitude/main/Statistic_Files/4det/PHASE_TIME_AMP_L1H1V1K1_FLOW.h5)

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
