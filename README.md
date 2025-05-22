# nmdare-processing

Defines the processing pipeline for the NMDARE dataset of von Schwanenflug et al. (2023)

The directories specified in `config/config.yaml` need to be changed to match the system this is running on.

To run the pipeline, create a directory called `bids`, put your data there in bids format, and in the terminal run `snakemake --cores 8` (or whatever the desired number of cores is)