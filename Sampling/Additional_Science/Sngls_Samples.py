"""
Create a file containing the time, phase, amplitude ratio and snr correlations between two
or more detectors for signals by doing a simple monte-carlo.

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
parser.add_argument('--relative-sensitivities', nargs='+', type=float,
                    help="Numbers proportional to horizon distance or "
                         "expected SNR at fixed distance, one for each ifo")
parser.add_argument('--seed', type=int, default=124)
parser.add_argument('--output-file', required=True)
parser.add_argument('--batch-size', type=int, default=1000000)
parser.add_argument('--samples', type=float, default=500000)

args = parser.parse_args()

if len(args.relative_sensitivities) != len(args.ifos):
    parser.error('--relative-sensitivities requires one numerical argument '
                 'for each detector')


d = {ifo: pycbc.detector.Detector(ifo) for ifo in args.ifos}

pycbc.init_logging(args.verbose)

np.random.seed(args.seed)
size = args.batch_size


# Use the first detector as a reference. The reference ifo is used 
# to get the correct symmetries when measuring dt, dp and sr for the triggers.
f = h5py.File(args.output_file, 'w')
ifo0 = args.ifos[0]
counts = defaultdict(list)

l = 0
nsamples = 0
all_keys = []
while len(all_keys)<=args.samples:
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
    for rs, ifo in zip(args.relative_sensitivities, args.ifos):
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
        
        

    # Organise the data
    bind = []
    keep = None

    snr_ref = np.log(data[ifo0]['snr'])
    bind += [snr_ref]
        
    
    # Applying thresholding, individual detector SNR > 4,

    keep = None 
    for ifo in args.ifos:
        if keep is None:
            keep = (data[ifo]['snr']>= 4 )
        else:
            keep = keep & (data[ifo]['snr']>= 4 )

    #Calculate and sum the weights for each bin
    # use first ifo as reference for weights
    bind = [a[keep] for a in bind]

     
    for key in zip(*bind):
        all_keys.append(key)

    ol = l
    l = len(all_keys)
    logging.info('%s, %s, %s, %s', l, l - ol, (l - ol) / float(size),
                 l / float(nsamples))




logging.info('Converting to numpy arrays')
keys = np.array(all_keys)

# Assiging names to each paramater.
field_names = []
field_names.extend([f'refsnr']
)
pdtype = [(name, 'float32') for name in field_names]


keys_bin = np.zeros(len(keys), dtype=pdtype)
for i, name in enumerate(field_names):
    keys_bin[name] = keys[:, i]

logging.info('Writing results to file')
f.create_dataset('%s/param_bin' % ifo0, data=keys_bin, compression='gzip',
             compression_opts=7)

f.attrs['sensitivity_ratios'] = args.relative_sensitivities
f.attrs['ifos'] = args.ifos
f.attrs['stat'] = 'MLtraining_samples_%s' % ''.join(args.ifos)

 
logging.info('Done')
