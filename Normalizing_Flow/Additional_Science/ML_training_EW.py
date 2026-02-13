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
    data_29 = {}
    data_32 = {}
    data_38 = {}
    data_44 = {}
    data_49 = {}
    data_56 = {}
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
            data_29[f"{key}"] = f[ref_ifo]["param_bin_29"][key][:]
            data_32[f"{key}"] = f[ref_ifo]["param_bin_32"][key][:]
            data_38[f"{key}"] = f[ref_ifo]["param_bin_38"][key][:]
            data_44[f"{key}"] = f[ref_ifo]["param_bin_44"][key][:]
            data_49[f"{key}"] = f[ref_ifo]["param_bin_49"][key][:]
            data_56[f"{key}"] = f[ref_ifo]["param_bin_56"][key][:]
    
    # Organise data and give bounds used.
    data_array_29 = np.array([v for v in data_29.values()]).T
    data_array_32 = np.array([v for v in data_32.values()]).T
    data_array_38 = np.array([v for v in data_38.values()]).T
    data_array_44 = np.array([v for v in data_44.values()]).T
    data_array_49 = np.array([v for v in data_49.values()]).T
    data_array_56 = np.array([v for v in data_56.values()]).T
    print(len(keys))
    torch.set_default_dtype(torch.float64)
    def create_bounds(data_array_29, data_array_32, data_array_38, data_array_44, data_array_49, data_array_56):
        # Both should have the same number of dimensions
        n_dims = data_array_29.shape[1]
        bounds = []
        smin = np.array([])
        smax = np.array([])
        
        for i in range(n_dims):
            # Calculate the global min/max across both arrays for this dimension
            global_min = min(data_array_29[:, i].min(), data_array_32[:, i].min(), data_array_38[:, i].min(), data_array_44[:, i].min(), data_array_49[:, i].min(), data_array_56[:, i].min())
            global_max = max(data_array_29[:, i].max(), data_array_32[:, i].max(), data_array_38[:, i].max(), data_array_44[:, i].max(), data_array_49[:, i].max(), data_array_56[:, i].max())
            
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
    bounds, smin, smax = create_bounds(data_array_29, data_array_32, data_array_38, data_array_44, data_array_49, data_array_56)
    datasets = {
    29.0: data_array_29,
    32.0: data_array_32,
    38.0: data_array_38,
    44.0: data_array_44,
    49.0: data_array_49,
    56.0: data_array_56
}
    # Train the Flow on the data.
    if len(ifos) == 2:
        flow = NormalizingFlow(len(keys), bounds=bounds, n_neurons=10, num_bins=4, conditions=1)
        history = flow.fit(datasets, n_samples=20000)

    srmin = min(smin)
    srmax = max(smax)
    p_29 = flow.prob(data_array_29, condition=np.full((len(data_array_29), 1), 29.0))
    p_32 = flow.prob(data_array_32, condition=np.full((len(data_array_32), 1), 32.0))
    p_38 = flow.prob(data_array_38, condition=np.full((len(data_array_38), 1), 38.0))
    p_44 = flow.prob(data_array_44, condition=np.full((len(data_array_44), 1), 44.0))
    p_49 = flow.prob(data_array_49, condition=np.full((len(data_array_49), 1), 49.0))
    p_56 = flow.prob(data_array_56, condition=np.full((len(data_array_56), 1), 56.0))

    hist_max = max(p_29.max(), p_32.max(), p_38.max(), p_44.max(), p_49.max(), p_56.max())
    # Save the model paramters to a file to be later used as a lookup.
    ml_stat = MLStatistic(model=flow, metadata={"ifos": ifos, "relfac": relfac, "stat": "phasetd_newsnr_%s" % ''.join(ifos), "smin": srmin, "smax": srmax, "hist_max": hist_max })
    ml_stat.to_file("../../Files/EW/PHASE_TIME_AMP_%s_EW.h5" % ''.join(ifos), group_name="model")
