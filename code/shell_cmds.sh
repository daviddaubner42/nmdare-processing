fmriprep-docker \
    ~/Desktop/nmdare-data-fmriprep/bids \
    ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep \
    participant \
    --fs-license-file ~/Desktop/nmdare-data-fmriprep/derivatives/freesurfer/license.txt \
    --participant_label LEGK010 \
    --cifti-output 

docker run -ti --rm \
    -v ~/Desktop/nmdare-data-fmriprep/bids:/data:ro \
    -v ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep:/out \
    -v ~/Desktop/nmdare-data-fmriprep/derivatives/freesurfer/license.txt:/opt/freesurfer/license.txt \
    nipreps/fmriprep:latest \
    /data /out participant \
    --fs-license-file /opt/freesurfer/license.txt \
    --participant_label LENMDA001 \
    --cifti-output

ciftify_recon_all sub-LEGK010 \
    --ciftify-work-dir ~/Desktop/nmdare-data-fmriprep/derivatives/ciftify \
    --fs-subjects-dir ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep/sourcedata/freesurfer

docker run -ti --rm \
    -v ~/Desktop/nmdare-data-fmriprep/bids:/data:ro \
    -v ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify:/out \
    -v ~/Desktop/nmdare-data-fmriprep/derivatives/freesurfer/license.txt:/opt/freesurfer/license.txt \
    tigrlab/fmriprep_ciftify:v1.3.2-2.3.3 \
    /data /out participant \
    --participant_label LEGK011 \
    --fs-license /opt/freesurfer/license.txt \
    --fmriprep-args "--skip_bids_validation --n_cpus 10"

mkdir ~/Desktop/nmdare-data-fmriprep/derivatives/wb_command

wb_command -cifti-parcellate \
    ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify/ciftify/sub-LEGK011/MNINonLinear/Results/task-rest_desc-preproc/task-rest_desc-preproc_Atlas_s0.dtseries.nii \
    ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify/ciftify/sub-LEGK011/sub-LEGK011.aparc.dlabel.nii \
    COLUMN \
    ~/Desktop/nmdare-data-fmriprep/derivatives/wb_command/sub-LEGK011/sub-LEGK011_task-rest_timeseries.ptseries.nii

# ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify/ciftify/sub-LEGK011/MNINonLinear/fsaverage_LR32k/sub-LEGK011.aparc.32k_fs_LR.dlabel.nii \

wb_command -cifti-correlation \
    ~/Desktop/nmdare-data-fmriprep/derivatives/wb_command/sub-LEGK011/sub-LEGK011_task-rest_timeseries.ptseries.nii \
    ~/Desktop/nmdare-data-fmriprep/derivatives/wb_command/sub-LEGK011/sub-LEGK011_task-rest_boldmap.pconn.nii


ciftify_vol_result sub-LEGK011 \
    /Users/brainsimulation/Desktop/nmdare-data-fmriprep/code/tpl-MNI152Nlin2009c_atlas-DesikanKilliany_desc-ranked_dseg.nii.gz \
    ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify/ciftify/sub-LEGK011/sub-LEGK011.aparc.dscalar.nii \
    --ciftify-work-dir ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify/ciftify \
    --integer-labels --resample-nifti

wb_command -cifti-label-import \
    ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify/ciftify/sub-LEGK011/sub-LEGK011.aparc.dscalar.nii \
    '' \
    ~/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify/ciftify/sub-LEGK011/sub-LEGK011.aparc.dlabel.nii

docker run -ti --rm \
    -v /Users/brainsimulation/Desktop/nmdare-data-fmriprep/code/:/code \
    --entrypoint /code/ciftify_entrypoint.sh \
    -v /Users/brainsimulation/Desktop/nmdare-data-fmriprep/code/tpl-MNI152Nlin2009c_atlas-DesikanKilliany_desc-ranked_dseg.nii.gz:/code/nifti_atlas.nii.gz \
    -v /Users/brainsimulation/Desktop/nmdare-data-fmriprep/derivatives/fmriprep_ciftify/ciftify:/ciftify \
    tigrlab/fmriprep_ciftify:v1.3.2-2.3.3 \
    sub-LEGK011 \
    /code/nifti_atlas.nii.gz \
    /ciftify/sub-LEGK011/sub-LEGK011.aparc.dscalar.nii \
    --ciftify-work-dir /ciftify \
    --integer-labels --resample-nifti