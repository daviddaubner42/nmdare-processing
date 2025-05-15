import os

"""
Converts all LE subjects into BIDS.
Needs to be run at the level of folder containing both the dicom and nifti folders
"""

# Path to the dicom folder
dicom_folder = 'dicom'

# Get a list of all folder names in the dicom folder
folder_names = [name for name in os.listdir(dicom_folder) if os.path.isdir(os.path.join(dicom_folder, name))]

tbp = []
nice_names = []
for name in folder_names:
    if 'LE' in name:
        tbp.append(name)
        nice_names.append(name[:-3])

for i,fname in enumerate(tbp):
    os.system(f'heudiconv --files dicom/{fname}/*/*/*.dcm -o nifti/ -f nifti/code/le_heuristic.py -s {nice_names[i]} -c dcm2niix -b --minmeta --overwrite')
