import argparse
import numpy as np
from copy import deepcopy
import torch
import h5py

from ml_stat_universal import MLStatistic, NormalizingFlow


def build_keys(ifos, ref_ifo):
    other_ifos = deepcopy(ifos)
    other_ifos.remove(ref_ifo)
    keys = []
    for ifo in other_ifos:
        keys.extend([f"dt_{ifo}", f"dp_{ifo}", f"sr_{ifo}"])
    return keys


def is_param_bin_group(name: str) -> bool:
    return name == "param_bin" or name.startswith("param_bin_")


def parse_cond_from_group(name: str):
    """
    Returns:
      (cond_value, is_unconditional)
    """
    if name == "param_bin":
        return None, True
    # name is param_bin_<something>
    suffix = name.split("param_bin_", 1)[-1]
    try:
        return float(suffix), False
    except ValueError as e:
        raise ValueError(
            f"Found group '{name}' but suffix '{suffix}' is not numeric. "
            f"Rename to param_bin_<number> (e.g. param_bin_0, param_bin_1, param_bin_29)."
        ) from e


def load_datasets_from_file(f: h5py.File, ref_ifo: str, keys):
    """
    Returns:
      datasets: dict[float, np.ndarray]
      n_conditions: int (0 or 1)
      condition_type: "none" | "numeric"
      unconditional_present: bool
    """
    ref = f[ref_ifo]

    group_names = [n for n in ref.keys() if is_param_bin_group(n)]
    if not group_names:
        raise ValueError(f"No param_bin / param_bin_* groups found under '{ref_ifo}'")

    datasets = {}
    unconditional_present = False
    conditional_present = False

    for gname in sorted(group_names):
        cond, is_uncond = parse_cond_from_group(gname)
        g = ref[gname]

        # build (N, D)
        arr = np.array([g[k][:] for k in keys]).T

        if is_uncond:
            unconditional_present = True
            # store under a dummy key, but we will train unconditional (conditions=0)
            datasets[0.0] = arr
        else:
            conditional_present = True
            datasets[float(cond)] = arr

    if unconditional_present and conditional_present:
        raise ValueError(
            "This file contains BOTH 'param_bin' (unconditional) and 'param_bin_<number>' (conditional). "
            "Keep them separate. Unconditional is p(x); conditional is p(x|c)."
        )

    n_conditions = 0 if unconditional_present else 1
    condition_type = "none" if n_conditions == 0 else "numeric"
    return datasets, n_conditions, condition_type, unconditional_present


def merge_datasets(dst: dict, src: dict):
    """
    Concatenate arrays for matching condition keys.
    """
    for k, v in src.items():
        if k in dst:
            dst[k] = np.vstack([dst[k], v])
        else:
            dst[k] = v
    return dst


def create_global_bounds(datasets: dict, n_dims: int):
    """
    Bounds across ALL datasets, with dp fixed to [0, 2π].
    Returns: bounds (D,2) float32, srmin, srmax (linear space)
    """
    bounds = []
    smins = []
    smaxs = []

    for i in range(n_dims):
        dim_min = min(d[:, i].min() for d in datasets.values())
        dim_max = max(d[:, i].max() for d in datasets.values())

        if i % 3 == 1:  # dp (phase)
            bounds.append([0.0, 2.0 * np.pi])
        elif i % 3 == 2:  # sr (usually log(sr) in your training data)
            bounds.append([dim_min - 1e-6, dim_max + 1e-6])
            smins.append(np.exp(dim_min - 1e-6))
            smaxs.append(np.exp(dim_max + 1e-6))
        else:  # dt
            bounds.append([dim_min - 1e-6, dim_max + 1e-6])

    bounds = np.array(bounds, dtype=np.float32)
    srmin = float(np.min(smins)) if smins else 0.0
    srmax = float(np.max(smaxs)) if smaxs else 0.0
    return bounds, srmin, srmax


def compute_hist_max(flow, datasets: dict, n_conditions: int):
    """
    max probability density across all datasets.
    """
    hmax = -np.inf
    for cond, arr in datasets.items():
        if n_conditions == 0:
            p = flow.prob(arr)
        else:
            c = np.full((len(arr), 1), float(cond), dtype=np.float64)
            p = flow.prob(arr, condition=c)
        hmax = max(hmax, float(np.max(p)))
    return float(hmax)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-files", nargs="+", required=True,
                        help="Input HDF5 files containing param_bin / param_bin_<number> groups")
    parser.add_argument("--output-file", required=True,
                        help="Output model file (HDF5) written by MLStatistic.to_file")
    parser.add_argument("--group-name", default="model",
                        help="HDF5 group name to write the model into (default: model)")

    # Training hyperparams (defaults match your examples)
    parser.add_argument("--n-samples", type=int, default=20000,
                        help="n_samples passed into flow.fit(...)")
    parser.add_argument("--n-neurons", type=int, default=10)
    parser.add_argument("--num-bins", type=int, default=4)
    parser.add_argument("--conditions", type=int, default=None,
                        help="Override auto-detected conditions (0 or 1). Usually leave unset.")
    args = parser.parse_args()

    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.set_default_dtype(torch.float64)

    merged = None
    ifos = None
    relfac = None
    n_conditions = None
    condition_type = None
    keys = None

    # Read and merge all input files
    for fname in args.input_files:
        with h5py.File(fname, "r") as f:
            ifos_here = list(f.attrs["ifos"])
            ref_ifo = ifos_here[0]
            keys_here = build_keys(ifos_here, ref_ifo)
            relfac_here = f.attrs["sensitivity_ratios"]

            datasets_here, ncond_here, ctype_here, _ = load_datasets_from_file(f, ref_ifo, keys_here)

            if merged is None:
                merged = {k: v for k, v in datasets_here.items()}
                ifos = ifos_here
                relfac = relfac_here
                n_conditions = ncond_here
                condition_type = ctype_here
                keys = keys_here
            else:
                if ifos_here != ifos:
                    raise ValueError(f"IFO mismatch across inputs: {ifos_here} vs {ifos}")
                if keys_here != keys:
                    raise ValueError("Key mismatch across inputs (unexpected).")
                if ncond_here != n_conditions:
                    raise ValueError("Cannot mix conditional and unconditional training files in one run.")
                merged = merge_datasets(merged, datasets_here)

    if merged is None:
        raise RuntimeError("No data loaded (this should be impossible).")

    # Override conditions if requested
    if args.conditions is not None:
        if args.conditions not in (0, 1):
            raise ValueError("--conditions must be 0 or 1")
        n_conditions = args.conditions
        condition_type = "none" if n_conditions == 0 else "numeric"

    # Build bounds from merged datasets
    any_arr = next(iter(merged.values()))
    n_dims = any_arr.shape[1]
    bounds, srmin, srmax = create_global_bounds(merged, n_dims)

    # Train
    flow = NormalizingFlow(
        dims=n_dims,
        bounds=bounds,
        n_neurons=args.n_neurons,
        num_bins=args.num_bins,
        conditions=n_conditions
    )
    _history = flow.fit(merged, n_samples=args.n_samples)

    # hist_max and optional binary ratio
    hist_max = compute_hist_max(flow, merged, n_conditions=n_conditions)

    on_vs_off = None
    if n_conditions == 1 and (0.0 in merged) and (1.0 in merged):
        on_vs_off = len(merged[1.0]) / max(1, len(merged[0.0]))

    meta = {
        "ifos": ifos,
        "relfac": relfac,
        "stat": "phasetd_newsnr_%s" % "".join(ifos),
        "smin": srmin,
        "smax": srmax,
        "hist_max": hist_max,
        "condition_type": condition_type,
        "condition_values": np.array(sorted(merged.keys()), dtype=np.float64),
    }
    if on_vs_off is not None:
        meta["on_vs_off"] = float(on_vs_off)

    ml_stat = MLStatistic(model=flow, metadata=meta)
    ml_stat.to_file(args.output_file, group_name=args.group_name)

    print("Wrote model to:", args.output_file)
    print("IFOs:", ifos)
    print("n_dims:", n_dims)
    print("conditions:", n_conditions, f"({condition_type})")
    print("condition_values:", sorted(merged.keys()))
    if on_vs_off is not None:
        print("on_vs_off:", on_vs_off)
    print("hist_max:", hist_max)


if __name__ == "__main__":
    main()