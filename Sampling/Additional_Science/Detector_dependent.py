"""
Create a file containing the time, phase, amplitude ratio and snr correlations between two
or more detectors for signals by doing a simple monte-carlo. This version also contains information on which detectors were
turned on for each sample.

Output is the relative amplitude, time, phase and snr as compared to a reference
IFO. The output file contains a continuous distribution of samples which can then be used to train a Normalizing Flow model.
"""


import argparse, h5py, numpy as np, pycbc.detector, logging
from numpy.random import uniform, normal
from copy import deepcopy
from collections import defaultdict


parser = argparse.ArgumentParser(description=__doc__)
pycbc.add_common_pycbc_options(parser)
parser.add_argument('--ifos', nargs='+',
                    help="The ifos to generate a histogram for")
parser.add_argument('--all-ifos', nargs='+',
                    help="All ifos in the network")
parser.add_argument('--relative-sensitivities', nargs='+', type=float,
                    help="Numbers proportional to horizon distance or "
                         "expected SNR at fixed distance, one for each ifo")
parser.add_argument('--seed', type=int, default=124)
parser.add_argument('--output-file', required=True)
parser.add_argument('--batch-size', type=int, default=1000000)
parser.add_argument('--samples', type=float, default=500000)
parser.add_argument('--phase-uncertainty', type=float, default=2.2,
                    help="Scale factor for phase uncertainty model")
parser.add_argument('--bandwidth', type=float, default=30.,
                    help="Effective bandwidth of the signal in Hz")
parser.add_argument('--time-phase-correlation', type=float, default=0.86,
                    help="Correlation coefficient between time and phase "
                         "measurement uncertainties")
args = parser.parse_args()

if len(args.relative_sensitivities) != len(args.all_ifos):
    parser.error('--relative-sensitivities requires one numerical argument '
                 'for each detector')


d = {ifo: pycbc.detector.Detector(ifo) for ifo in args.all_ifos}

pycbc.init_logging(args.verbose)

np.random.seed(args.seed)
size = args.batch_size


# Use the first detector as a reference. The reference ifo is used 
# to get the correct symmetries when measuring dt, dp and sr for the triggers.
f = h5py.File(args.output_file, 'w')
ifo0 = args.ifos[0]

# Detectors in the network that are NOT the reference (for dt, dp, sr calculations)
other_ifos = [ifo for ifo in args.ifos if ifo != ifo0]

# Detectors in the network that are NOT in the active 'ifos' list
dependent_ifos = [ifo for ifo in args.all_ifos if ifo not in args.ifos]

counts = defaultdict(list)

l = 0
nsamples = 0
all_keys_on = []
all_keys_off = []
while len(all_keys_on) + len(all_keys_off) <= args.samples:
    nsamples += size
    logging.info('generating %s samples', size)

    # Choose random sky location and polarizations from
    # an isotropic population. Distance is drawn from a 
    # squared power law distribution. D_max is chosen 
    # such that the SNR tail is normlaized to commonly 
    # commonly used values.
    ra = uniform(0, 2 * np.pi, size=size)
    dec = np.arccos(uniform(-1., 1., size=size)) - np.pi/2
    inc = np.arccos(uniform(-1., 1., size=size))
    pol = uniform(0, 2 * np.pi, size=size)
    ic = np.cos(inc)
    ip = 0.5 * (1.0 + ic * ic)
    D_max=0.6 * np.min(args.relative_sensitivities)
    uniform_random = np.random.uniform(0, 1, size=size)
    distance = D_max * (uniform_random)**(1/3) 


    # calculate the toa, poa, and amplitude of each sample,
    # including uncertainties in measurements.
    data = {}
    for rs, ifo in zip(args.relative_sensitivities, args.all_ifos):
        data[ifo] = {}
        fp, fc = d[ifo].antenna_pattern(ra, dec, pol, 0)
        sp, sc = fp * ip, fc * ic
        snr_sp = (rs*sp/distance) 
        snr_sc = (rs*sc/distance) 
        fsize = snr_sp.shape
        # Add noise to the SNR measurements
        normal_sp = normal(scale=1, size=fsize)
        normal_sc = normal(scale=1, size=fsize)
        snr_sp += normal_sp
        snr_sc += normal_sc
        data[ifo]['snr'] = (snr_sp**2+snr_sc**2)**0.5
        # Add noise to the phase and time measurements
        # Values obtained from modelling time and phase unc, t_unc given by Fairhurst 2009
        p_unc = args.phase_uncertainty/data[ifo]['snr']
        t_unc = 1/(2*np.pi*args.bandwidth*data[ifo]['snr'])
        rho = args.time_phase_correlation
        # Cholensky Decomposition
        l22_factor = np.sqrt(1.0 - rho**2)
        z_p = normal(size=fsize)
        z_t = normal(size=fsize)
        normal_dp = p_unc * z_p
        normal_dt = (rho * t_unc * z_p) + (t_unc * l22_factor * z_t)
        data[ifo]['p'] = (np.arctan2(snr_sc, snr_sp) + normal_dp) % (2. * np.pi)
        data[ifo]['t'] = d[ifo].time_delay_from_earth_center(ra, dec, 0) + normal_dt
        

    # Organise the data
    bind = []
    keep_off = None
    keep_on = None
    for ifo1 in other_ifos:
        dt = (data[ifo0]['t'] - data[ifo1]['t'])
        dp = (data[ifo0]['p'] - data[ifo1]['p']) % (2. * np.pi)
        sr = np.log(data[ifo1]['snr'] / data[ifo0]['snr'])
        dtbin = dt
        dpbin = dp
        srbin = sr
        bind += [dtbin, dpbin, srbin]

    snr_ref = np.log(data[ifo0]['snr'])
    bind += [snr_ref]
        
    
    # Applying thresholding, individual detector SNR > 4,

    keep_off = None 
    for ifo in args.ifos:
        if keep_off is None:
            keep_off = (data[ifo]['snr']>= 4 )
        else:
            keep_off = keep_off & (data[ifo]['snr']>= 4 )

    keep_on = None 
    for ifo in args.ifos:
        if keep_on is None:
            keep_on = (data[ifo]['snr']>= 4 )
        else:
            keep_on = keep_on & (data[ifo]['snr']>= 4 )
    for ifo in dependent_ifos:
        if keep_on is None:
            keep_on = (data[ifo]['snr']< 4 )
        else:
            keep_on = keep_on & (data[ifo]['snr']< 4 )






    #Calculate and sum the weights for each bin
    # use first ifo as reference for weights
    bind_off = [a[keep_off] for a in bind]
    bind_on = [a[keep_on] for a in bind]

     
    all_keys_off.extend(zip(*bind_off))
    all_keys_on.extend(zip(*bind_on))

    l = len(all_keys_on) + len(all_keys_off)
    logging.info(f'Total samples collected: {l} (On: {len(all_keys_on)}, Off: {len(all_keys_off)})')




logging.info('Converting to numpy arrays')

# Define the structured dtype (this part is fine as you had it)
field_names = []
for ifo in other_ifos:
    field_names.extend([f'dt_{ifo}', f'dp_{ifo}', f'sr_{ifo}'])
field_names.append('refsnr')
pdtype = [(name, 'float32') for name in field_names]

def create_structured_array(data_list, dtype, names):
    data_np = np.array(data_list)
    structured_array = np.zeros(len(data_np), dtype=dtype)
    for i, name in enumerate(names):
        structured_array[name] = data_np[:, i]
    return structured_array

logging.info('Writing results to file')

# Process and save "ON" samples
if all_keys_on:
    keys_on_bin = create_structured_array(all_keys_on, pdtype, field_names)
    f.create_dataset(f'{ifo0}/param_bin_1', data=keys_on_bin, 
                     compression='gzip', compression_opts=7)

# Process and save "OFF" samples
if all_keys_off:
    keys_off_bin = create_structured_array(all_keys_off, pdtype, field_names)
    f.create_dataset(f'{ifo0}/param_bin_0', data=keys_off_bin, 
                     compression='gzip', compression_opts=7)

# Save metadata
f.attrs['sensitivity_ratios'] = args.relative_sensitivities
f.attrs['ifos'] = args.ifos
f.attrs['stat'] = 'MLtraining_samples_%s' % ''.join(args.ifos)
f.close()
 
logging.info('Done')
