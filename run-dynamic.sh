#!/bin/sh

echo $SLURM_LOCALID
echo $SLURMD_NODENAME
#echo $LD_LIBRARY_PATH

# Everynode needs to copy data locally and set symlink once
if [ "$SLURM_LOCALID" == "0" ]
then
	~/copy-data.sh
else
	sleep 60 #Wait for other process to copy data
fi

python keras-tuner-dynamic.py > keras-tuner-dynamic-$SLURMD_NODENAME-$SLURM_LOCALID.log 2>&1
