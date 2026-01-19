import argparse, numpy as np, logging
from collections import defaultdict
from copy import deepcopy
from ml_stat import MLStatistic
from ml_stat import NormalizingFlow
import torch
import h5py

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input-files', nargs='+', required=True, help="Input files to train ML model on")
args = parser.parse_args()

files = args.input_files
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
# Read in parameter data from files. Also list of ifos and reference detector.
for file in files:
    data = {}
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
            data[f"{key}"] = f[ref_ifo]["param_bin"][key][:]
    # Organise data and give bounds used.
    data_array = np.array([v for v in data.values()]).T
    torch.set_default_dtype(torch.float64)
    def create_bounds(data_array):
        n_dims = data_array.shape[1]
        bounds = []
        smin = np.array([])
        smax = np.array([])
        
        for i in range(n_dims):
            if i % 3 == 1:  # every second dimension (Phase)
                bounds.append([0, 2*np.pi])
            elif i % 3 == 2:
                bounds.append([data_array[:, i].min() - 1e-6, 
                            data_array[:, i].max() + 1e-6])
                smin =np.append(smin, np.exp(data_array[:, i].min() - 1e-6))
                smax = np.append(smax,np.exp(data_array[:, i].max() + 1e-6))
            else:
                bounds.append([data_array[:, i].min() - 1e-6, 
                            data_array[:, i].max() + 1e-6])
        
        return np.array(bounds, dtype=np.float32), smin, smax

    # Train the Flow on the data.
    bounds, smin, smax = create_bounds(data_array)
    if len(ifos) == 2:
        flow = NormalizingFlow(len(keys), bounds=bounds, n_neurons=10, num_bins=4)
        history = flow.fit(data_array, n_samples=500000)
    elif len(ifos) == 3:
        flow = NormalizingFlow(len(keys), bounds=bounds, n_neurons=80, num_bins=15)
        history = flow.fit(data_array, n_samples=500000)
    elif len(ifos) == 4:
        flow = NormalizingFlow(len(keys), bounds=bounds, n_neurons=128, num_bins=20)
        history = flow.fit(data_array, n_samples=700000)
    elif len(ifos) == 5:
        flow = NormalizingFlow(len(keys), bounds=bounds, n_neurons=140, num_bins=25)
        history = flow.fit(data_array, n_samples=1000000)

    srmin = min(smin)
    srmax = max(smax)
    hist_max = max(flow.prob(data_array))
    # Save the model paramters to a file to be later used as a lookup.
    ml_stat = MLStatistic(model=flow, metadata={"ifos": ifos, "relfac": relfac, "stat": "phasetd_newsnr_%s" % ''.join(ifos), "smin": srmin, "smax": srmax, "hist_max": hist_max})
    ml_stat.to_file("../Files/PHASE_TIME_AMP_%s_FLOW.h5" % ''.join(ifos), group_name="model")
