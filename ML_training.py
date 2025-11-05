import argparse, numpy as np, logging
from collections import defaultdict
from copy import deepcopy
from ml_stat import MLStatistic
from ml_stat import NormalizingFlow

parser = argparse.ArgumentParser(description=__doc__)
pycbc.add_common_pycbc_options(parser)
parser.add_argument('--input-files', nargs='+', required=True, help="Input files to train ML model on")
args = parser.parse_args()

files = args.input_files

for file in files:
    with h5py.File(file, "r") as f:
        ifos = f.attrs["ifos"]
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
            data[f"{key}"] = f[ifo]["param_bin"][key][:]
    data_array = np.array([v for v in data.values()]).T
    bounds = np.array([data_array.min(0)-1e-6, data_array.max(0)+1e-6]).T
    flow = NormalizingFlow(3, bounds=bounds)
    history = flow.fit(data_array, n_samples=100000)
    ml_stat = MLStatistic(model=flow, metadata={"ifos": ifos, "relfac": relfac, "stat": "phasetd_newsnr_%s" % ''.join(ifos) })
    ml_stat.to_file("phasetd_newsnr_%s.h5" % ''.join(ifos), group_name="model")