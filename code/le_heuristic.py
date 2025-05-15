from __future__ import annotations

import logging
from typing import Optional

from heudiconv.utils import SeqInfo

lgr = logging.getLogger("heudiconv")


def create_key(
    template: Optional[str],
    outtype: tuple[str, ...] = ("nii.gz",),
    annotation_classes: None = None,
) -> tuple[str, tuple[str, ...], None]:
    if template is None or not template:
        raise ValueError("Template must be a valid format string")
    return (template, outtype, annotation_classes)


def infotodict(
    seqinfo: list[SeqInfo],
) -> dict[tuple[str, tuple[str, ...], None], list[str]]:
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    data = create_key("run{item:03d}")

    # anat
    t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    t2w = create_key('sub-{subject}/anat/sub-{subject}_T2w')

    # func
    bold = create_key('sub-{subject}/func/sub-{subject}_task-rest_bold')

    # dwi
    dwi = create_key('sub-{subject}/dwi/sub-{subject}_dwi')

    # fmap
    fmap_mag = create_key('sub-{subject}/fmap/sub-{subject}_magnitude')
    fmap_phase = create_key('sub-{subject}/fmap/sub-{subject}_phasediff')

    info = {
        t1w: [],
        t2w: [],
        fmap_mag: [],
        fmap_phase: [],
        bold: [],
        dwi: [],
    }

    for idx, s in enumerate(seqinfo):
        print(s.image_type)
        if "MPRAGE" in s.series_description:
            info[t1w].append(s.series_id)
        elif "t2_spc" in s.series_description:
            info[t2w].append(s.series_id)
        elif "BOLD" in s.series_description and "rest" in s.series_description:
            info[bold].append(s.series_id)
        elif "DTI" in s.series_description:
            info[dwi].append(s.series_id)
        elif "FieldMapping" in s.series_description and 'M' in s.image_type:
            info[fmap_mag].append(s.series_id)
        elif "FieldMapping" in s.series_description and 'P' in s.image_type:
            info[fmap_phase].append(s.series_id)

    return info