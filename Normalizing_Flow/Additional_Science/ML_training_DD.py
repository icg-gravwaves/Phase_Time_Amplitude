"""Training a Normalizing Flow model on the Phase, Time and Amplitude sampled data from simulated signals in multiple detectors.
 The model paramteters are saved to a file that can be later used to evaluate the probability density of triggers during the search. """


import argparse, numpy as np, logging
from collections import defaultdict
from copy import deepcopy
from ml_stat_universal import MLStatistic
from ml_stat_universal import NormalizingFlow
import torch
import h5py

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input-files', nargs='+', required=True, help="Input files to train ML model on")
args = parser.parse_args()

files = args.input_files
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
# Read in parameter data from files. Also list of ifos and reference detector, needed for evaluating triggers.
for file in files:
    data_on = {}
    data_off = {}
    with h5py.File(file, "r") as f:
        ifos = list(f.attrs["ifos"])
        ref_ifo = ifos[0]
        other_ifos = deepcopy(ifos)
        other_ifos.remove(ref_ifo)
        relfac = f.attrs["sensitivity_ratios"]
        keys = []
        for ifo in other_ifos:
            keys.extend([
                f"dt_{ifo}",
                f"dp_{ifo}",
                f"sr_{ifo}"
            ])
        for key in keys:
            data_on[f"{key}"] = f[ref_ifo]["param_bin_on"][key][:]
            data_off[f"{key}"] = f[ref_ifo]["param_bin_off"][key][:]
    # Organise data and give bounds used.
    data_array_on = np.array([v for v in data_on.values()]).T
    data_array_off = np.array([v for v in data_off.values()]).T
    on_vs_off = len(data_array_on) / len(data_array_off)

    
    torch.set_default_dtype(torch.float64)
    def create_bounds(data_on, data_off):
        # Both should have the same number of dimensions
        n_dims = data_on.shape[1]
        bounds = []
        smin = np.array([])
        smax = np.array([])
        
        for i in range(n_dims):
            # Calculate the global min/max across both arrays for this dimension
            global_min = min(data_on[:, i].min(), data_off[:, i].min())
            global_max = max(data_on[:, i].max(), data_off[:, i].max())
            
            if i % 3 == 1:  # Phase parameter
                bounds.append([0, 2*np.pi])
                
            elif i % 3 == 2: # Signal ratio parameter
                # Use the global min/max for the bounds
                bounds.append([global_min - 1e-6, global_max + 1e-6])
                
                # Use global min/max for the exponential scaling
                smin = np.append(smin, np.exp(global_min - 1e-6))
                smax = np.append(smax, np.exp(global_max + 1e-6))
                
            else: # Time parameter
                bounds.append([global_min - 1e-6, global_max + 1e-6])
        
        return np.array(bounds, dtype=np.float32), smin, smax

    # Find the bounds for each parameter as well as the maximum and minimum signal ratios in the training data. These are used to measure the volume later in the search.
    bounds, smin, smax = create_bounds(data_array_on, data_array_off)
    datasets = {
        1.0: data_array_on,
        0.0: data_array_off
    }
    # Train the Flow on the data.
    if len(ifos) == 2:
        flow = NormalizingFlow(len(keys), bounds=bounds, n_neurons=10, num_bins=4, conditions=1)
        history = flow.fit(datasets, n_samples=10000)
    elif len(ifos) == 3:
        flow = NormalizingFlow(len(keys), bounds=bounds, n_neurons=80, num_bins=15, conditions=0)
        history = flow.fit(datasets, n_samples=500000)
 

    srmin = min(smin)
    srmax = max(smax)
    p_on  = flow.prob(data_array_on,  condition=np.full((len(data_array_on), 1), 1.0))
    p_off = flow.prob(data_array_off, condition=np.full((len(data_array_off), 1), 0.0))

    hist_max = max(p_on.max(), p_off.max())
    # Save the model paramters to a file to be later used as a lookup.
    ml_stat = MLStatistic(model=flow, metadata={"ifos": ifos, "relfac": relfac, "stat": "phasetd_newsnr_%s" % ''.join(ifos), "smin": srmin, "smax": srmax, "hist_max": hist_max, "on_vs_off": on_vs_off})
    ml_stat.to_file("../../Files/Det_Dep/PHASE_TIME_AMP_%s_DD.h5.hdf" % ''.join(ifos), group_name="model")
