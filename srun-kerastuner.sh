#!/bin/sh

# ntasks = gpus+1
# gpus = total gpus across all nodes
srun --partition=gpu-debug --account=TG-ASC160050 --mpi=pmi2 --ntasks=9 \
    --nodes=2 --mem=96G --gpus=8 -t 00:30:00 --wait=0 --export=ALL --output=srun-kerastuner.out ~/run-dynamic.sh 
