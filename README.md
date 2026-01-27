# Phase_Time_Amplitude

Welcome! This project looks at using generative machine learning models called normlaizing flows for density evaluation in PyCBC searches for compact binary coalescences.
In this repository you can find the code used to both genertae samples and train a normalizing flow on those samples. In addition it alos contains ongoing work on how we incorporate uncertainities into the sampling.

Two PyCBC searhces were done during this project, one involving some modifications to how we sample but still using histogram-based density estimators, the other uses a normlazing flow trained on these modified samples. There are two separate sampling files to account for these as they are incorporated into the PyCBC serach in slightly different ways. If one wishes to replicate the searches, you would need to clone the MODIFIED AND PTA (normalizing flow) branches in this repository: https://github.com/SamInsley/pycbc.git, which make modifications to the exisiting PyCBC search to incorporat ethese methodologies.
