import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import os

def fc_matrix(ts):
    n = ts.shape[1]
    fc = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            fc[i, j] = np.corrcoef(ts[:, i], ts[:, j])[0, 1]
    return fc

def FCuCorrelation(FC1, FC2, fisher=True):
    """
    Computes the correlation between the upper triangular parts of two FC matrices.

    Parameters
    ----------
    FC1 : ndarray
        The first functional connectivity matrix (N, N).
    FC2 : ndarray
        The second functional connectivity matrix (N, N).
    fisher : bool, optional (default=True)
        If True, applies Fisher's z-transformation to the upper triangular elements.

    Returns
    -------
    float
        Pearson correlation between the upper triangular elements of FC1 and FC2.
    """
    u_idx = np.triu_indices_from(FC1, k=1)
    FCu1 = FC1.copy()[u_idx]
    FCu2 = FC2.copy()[u_idx]
    if fisher:
        FCu1 = np.arctanh(FCu1)
        FCu2 = np.arctanh(FCu2)
    FC_corr_upper = np.corrcoef(FCu1, FCu2)[0, 1]
    return FC_corr_upper

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("subid", help="The subject id")
parser.add_argument("ts_filename", help="The location of the region-wise timeseries file")
parser.add_argument("out_dir", help="The directory where the output should be stored")
args = parser.parse_args()

ts_fname=args.ts_filename
derivatives_dir=args.out_dir
sub=args.subid


os.makedirs(os.path.join(derivatives_dir, sub, "figs"), exist_ok=True)

time_series = nib.load(ts_fname).dataobj

# Truncate the first few volumes

static_fc = fc_matrix(time_series)
if "Glasser" in ts_fname:
    static_fc = np.delete(static_fc, [119, 299], 1)
    static_fc = np.delete(static_fc, [119, 299], 0)
np.fill_diagonal(static_fc, np.nan)

window_size = 40
window_step = 5

all_fcs = []
for i in range(0, time_series.shape[0] - window_size, window_step):
    window_ts = time_series[i:i + window_size, :]

    fc = fc_matrix(window_ts)
    if "Glasser" in ts_fname:
        fc = np.delete(fc, [119, 299], 1)
        fc = np.delete(fc, [119, 299], 0)
    np.fill_diagonal(fc, np.nan)

    all_fcs.append(fc)

n_fcs = len(all_fcs)

FCD = np.zeros((n_fcs, n_fcs))
for i in range(n_fcs):
    for j in range(n_fcs):
        FCD[i, j] = FCuCorrelation(all_fcs[i], all_fcs[j])

fcd_flattened = FCD.flatten()

if "Glasser" in ts_fname:
    pd.DataFrame(static_fc).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-Glasser_static_FC.csv"), index=False)
    plt.imshow(static_fc, cmap='viridis')
    plt.colorbar(label='Correlation')
    plt.title(f'Static FC Matrix: {sub}')
    plt.tight_layout()
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-Glasser_static_FC.png"))
    plt.close()

    pd.DataFrame(FCD).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-Glasser_FCD.csv"), index=False)
    plt.imshow(FCD, cmap='viridis')
    plt.colorbar(label='Correlation')
    plt.title(f'FCD Matrix: {sub}')
    plt.tight_layout()
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-Glasser_FCD.png"))
    plt.close()

    hist = plt.hist(fcd_flattened, bins=100, range=(0, 1))
    bin_counts = hist[0]
    pd.DataFrame(bin_counts).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-Glasser_FCD_histogram_counts.csv"), index=False)
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-Glasser_FCD_histogram.png"))
elif "4S156" in ts_fname:
    pd.DataFrame(static_fc).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-4S156_static_FC.csv"), index=False)
    plt.imshow(static_fc, cmap='viridis')
    plt.colorbar(label='Correlation')
    plt.title(f'Static FC Matrix: {sub}')
    plt.tight_layout()
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-4S156_static_FC.png"))
    plt.close()

    pd.DataFrame(FCD).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-4S156_FCD.csv"), index=False)
    plt.imshow(FCD, cmap='viridis')
    plt.colorbar(label='Correlation')
    plt.title(f'FCD Matrix: {sub}')
    plt.tight_layout()
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-4S156_FCD.png"))
    plt.close()

    hist = plt.hist(fcd_flattened, bins=100, range=(0, 1))
    bin_counts = hist[0]
    pd.DataFrame(bin_counts).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-4S156_FCD_histogram_counts.csv"), index=False)
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-4S156_FCD_histogram.png"))
else:
    pd.DataFrame(static_fc).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-unknown_static_FC.csv"), index=False)
    plt.imshow(static_fc, cmap='viridis')
    plt.colorbar(label='Correlation')
    plt.title(f'Static FC Matrix: {sub}')
    plt.tight_layout()
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-unknown_static_FC.png"))
    plt.close()
    
    pd.DataFrame(FCD).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-unknown_FCD.csv"), index=False)
    plt.imshow(FCD, cmap='viridis')
    plt.colorbar(label='Correlation')
    plt.title(f'FCD Matrix: {sub}')
    plt.tight_layout()
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-unknown_FCD.png"))
    plt.close()

    hist = plt.hist(fcd_flattened, bins=100, range=(0, 1))
    bin_counts = hist[0]
    pd.DataFrame(bin_counts).to_csv(os.path.join(derivatives_dir, sub, f"{sub}_seg-unknown_FCD_histogram_counts.csv"), index=False)
    plt.savefig(os.path.join(derivatives_dir, sub, "figs", f"{sub}_seg-unknown_FCD_histogram.png"))