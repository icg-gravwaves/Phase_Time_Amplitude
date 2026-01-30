"""
Create a file containing the time, phase and amplitude correlations between two
or more detectors for signals by doing a simple monte-carlo.

Output is the relative amplitude, time, and phase as compared to a reference
IFO. The output file contains a continuous distribution of samples which can then be used to train a Normalizing Flow model.
"""


import argparse, h5py, numpy as np, pycbc.detector, logging
from numpy.random import uniform, normal
from copy import deepcopy
from collections import defaultdict
from pycbc.waveform import get_fd_waveform
from pycbc.psd import aLIGOZeroDetHighPower
from scipy.interpolate import RectBivariateSpline


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
parser.add_argument('--phase-uncertainty', type=float, default=2.2,
                    help="Scale factor for phase uncertainty model")
parser.add_argument('--bandwidth', type=float, default=30.,
                    help="Effective bandwidth of the signal in Hz")
parser.add_argument('--time-phase-correlation', type=float, default=0.86,
                    help="Correlation coefficient between time and phase "
                         "measurement uncertainties")
args = parser.parse_args()

if len(args.relative_sensitivities) != len(args.ifos):
    parser.error('--relative-sensitivities requires one numerical argument '
                 'for each detector')


d = {ifo: pycbc.detector.Detector(ifo) for ifo in args.ifos}

pycbc.init_logging(args.verbose)

np.random.seed(args.seed)
size = args.batch_size

""" Bandwidth Calculation """

def bandwidth(m1,m2,f_lower=20.0, delta_f=1/4, f_final = 56):
    hp, hc = get_fd_waveform(approximant="IMRPhenomXPHM",
                            mass1=m1, mass2=m2,
                            f_lower=f_lower,
                            delta_f=delta_f,
                            f_final = f_final)
    f = hp.sample_frequencies.numpy()
    h_abs2 = np.abs(hp.numpy())**2
    psd = aLIGOZeroDetHighPower(len(hp), hp.delta_f, f_lower)
    psd=psd.numpy()
    mask = (f >= f_lower) & (psd > 0) & np.isfinite(psd)
    f, w = f[mask], h_abs2[mask] / psd[mask]
    norm = np.sum(w) * delta_f                      
    f_mean  = (np.sum(f * w) * delta_f) / norm      
    f2_mean = (np.sum((f**2) * w) * delta_f) / norm
    bw2 = f2_mean - f_mean**2
    bw = np.sqrt(max(float(bw2), 0.0))
    return bw

""" Building Interpolation Grid """

#Build up a grid of bandwidth values for different masses, the bandwidth in the sampler then uses this 
#grid to interpolate the bandwidth for given masses. It would take too long to compute the bandwidth
#for each sample with the number of samples we want to generate. 

grid_points = 40  
m_range = np.linspace(1, 80, grid_points)
z_grid = np.zeros((grid_points, grid_points))

for i, mi in enumerate(m_range):
    for j, mj in enumerate(m_range):
        if mj > mi: 
            z_grid[i, j] = bandwidth(mj, mi) 
        else:
            z_grid[i, j] = bandwidth(mi, mj)
interp_func = RectBivariateSpline(m_range, m_range, z_grid)


# Use the first detector as a reference. The reference ifo is used 
# to get the correct symmetries when measuring dt, dp and sr for the triggers.
f = h5py.File(args.output_file, 'w')
ifo0 = args.ifos[0]
other_ifos = deepcopy(args.ifos)
other_ifos.remove(ifo0)
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

    """ Mass Model """

    m1_samples = np.random.uniform(1, 150, size=size)
    m2_samples = np.random.uniform(1, 150, size=size)
    # Ensure m1 >= m2 for consistency
    mask = m2_samples > m1_samples
    m1_samples[mask], m2_samples[mask] = m2_samples[mask], m1_samples[mask]

    def chirp_mass(m1, m2):
        return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)

    """ Distance Model """

    D_max=0.6 * np.min(args.relative_sensitivities)
    uniform_random = np.random.uniform(0, 1, size=size)
    distance = D_max * (uniform_random)**(1/3) 


    """ Measuring Bandwidth for given masses"""
 
    bw = interp_func.ev(m1_samples, m2_samples)

    """ Signal Location and Orientation """

    ra = uniform(0, 2 * np.pi, size=size)
    dec = np.arccos(uniform(-1., 1., size=size)) - np.pi/2
    inc = np.arccos(uniform(-1., 1., size=size))
    pol = uniform(0, 2 * np.pi, size=size)
    ic = np.cos(inc)
    ip = 0.5 * (1.0 + ic * ic)



    # calculate the toa, poa, and amplitude of each sample,
    # including uncertainties in measurements.
    data = {}
    for rs, ifo in zip(args.relative_sensitivities, args.ifos):
        data[ifo] = {}
        fp, fc = d[ifo].antenna_pattern(ra, dec, pol, 0)
        sp, sc = fp * ip, fc * ic
        data[ifo]['amp'] = (sp**2+sc**2)**0.5*rs #Amplitude without uncertainities
        mass_distance_factor = ((chirp_mass(m1_samples, m2_samples)**(5/4))/distance)
        snr_sp = (rs*sp*mass_distance_factor) 
        snr_sc = (rs*sc*mass_distance_factor)
        data[ifo]['op'] = np.arctan2(snr_sc, snr_sp) #Phase without uncertainties
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
        t_unc = 1/(2*np.pi*bw*data[ifo]['snr'])
        rho = args.time_phase_correlation
        # Cholensky Decomposition, for a bivariate gaussian between time and phase
        l22_factor = np.sqrt(1.0 - rho**2)
        z_p = normal(size=fsize)
        z_t = normal(size=fsize)
        normal_dp = p_unc * z_p
        normal_dt = (rho * t_unc * z_p) + (t_unc * l22_factor * z_t)
        data[ifo]['p'] = (data[ifo]['op'] + normal_dp) % (2. * np.pi)
        data[ifo]['t'] = d[ifo].time_delay_from_earth_center(ra, dec, 0) + normal_dt
        

    # Organise the data
    bind = []
    keep = None
    for ifo1 in other_ifos:
        dt = (data[ifo0]['t'] - data[ifo1]['t'])
        dp = (data[ifo0]['p'] - data[ifo1]['p']) % (2. * np.pi)
        sr = np.log(data[ifo1]['snr'] / data[ifo0]['snr'])
        dtbin = dt
        dpbin = dp
        srbin = sr
        bind += [dtbin, dpbin, srbin]
        
            
    # Measure network SNR.
    snrs_sq=np.zeros(len(data[ifo0]['snr']))
    for ifo in args.ifos:
        snrs_sq += data[ifo]['snr']**2
    net_snr = snrs_sq**0.5
    
    # Applying thresholding, individual detector SNR > 5,
    # network SNR > 9.
    keep = None 
    for ifo in args.ifos:
        if keep is None:
            keep = (net_snr >= 9) & (data[ifo]['snr']>= 5 )
        else:
            keep = keep & (net_snr >= 9) & (data[ifo]['snr']>= 5 )

    #Calculate and sum the weights for each bin
    # use first ifo as reference for weights
    bind = [a[keep] for a in bind]

    # Ensure we arent getting a significant number of events within 5% of D_max
    dist = distance[keep]
    large_dis = 0
    for i in range(len(dist)):
        if dist[i]/D_max > .95:
            large_dis += 1
    if len(dist) == 0: 
        logging.warning("dist is empty, skipping the large distance check")
    else:
        if large_dis / len(dist) > 0.01:
            raise ValueError("Too many distances exceed 95% of the maximum allowed value")
     
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
for ifo in other_ifos:
    field_names.extend([
        f'dt_{ifo}',
        f'dp_{ifo}',
        f'sr_{ifo}'
        
    ])


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
