#!/bin/bash

mkdir $result_folder/demo_quick_start_$SLURM_PROCID
chmod 755 $result_folder/demo_quick_start_$SLURM_PROCID
ls /
python main.py
