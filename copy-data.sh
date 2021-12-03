cp /expanse/lustre/projects/sio134/jlin96/testCrucible/*.npy /scratch/dwalling/job_$SLURM_JOB_ID
cp /expanse/lustre/projects/sio134/jlin96/collabIngredients/*.npy /scratch/dwalling/job_$SLURM_JOB_ID

rm ~/data
ln -s /scratch/dwalling/job_$SLURM_JOB_ID ~/data
