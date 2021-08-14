#!/bin/bash

mkdir $result_folder/demo_quick_start$SLURM_NODEID
chmod 755 $result_folder/demo_quick_start_$SLURM_NODEID
python main.py