# kerastuner-slurm

## KT.yml
Ensure you launch srun-kerastuner.sh with the correct conda environment active.  Additionally, add to ~/.bashrc to load that environment.


## srun-kerastuner.sh
This is the sbatch script for launching the job and setting the total number of python process to run, the number of nodes and total gpu count


## run-dynamic.sh
This script ensures that each node has staged the input data, then launches the python processes.  It will be run --ntasks times.  Each node should have a process where slurm_localid = 0. It also outputs some diagnostic information for debugging.


## copy-data.sh
Ensures training/test data is staged appropriately


## keras-tuner-dynamic.py - def set_environment()
This method in python dynamically sets the correct keras tuner environment variables. We utilize the fact that each node will get a set of procs where slurm_localid from 0 to gpus-1.  One node, the first in the list of SLURM_NODELIST, will get a slurm_localid=num_gpus_per_node.


# Additional Notes

## Search Algorithm
For massively parallel searches, it is recommended to use the RandomSearch algorithm.  The other options have dependencies between trials, and it is unclear if they would efficiently utilize all available GPUs.  RandomSearch has good results in practice.

## Search Monitoring

As the job is running, you can open another terminal and find which nodes the job has allocated.

(KT) [dwalling@login01 ~]$ squeue - u dwalling

             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON) 

           6044873 gpu-debug run-dyna dwalling  R       0:57      2 exp-7-[59-60] 

With this information, you can the ssh to the nodes, example: ssh exp-7-60

Once on the node, you can use top, ps and nvidia-smi to monitor processes.

