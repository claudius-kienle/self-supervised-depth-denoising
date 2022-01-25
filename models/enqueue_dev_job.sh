#!/bin/bash
#SBATCH --partition=dev_gpu_4
#SBATCH --nodes=1
#SBATCH --cpus-per-task=40
#SBATCH --time=0:30:00
#SBATCH --mem=6000mb   
#SBATCH --gres=gpu:2
#SBATCH --export=ALL,EXECUTABLE=./train_models.sh
#SBATCH --output="train_models.out"
#SBATCH -J OpenMP_Test

#Usually you should set
export KMP_AFFINITY=compact,1,0
#export KMP_AFFINITY=verbose,compact,1,0 prints messages concerning the supported affinity
#KMP_AFFINITY Description: https://software.intel.com/en-us/node/524790#KMP_AFFINITY_ENVIRONMENT_VARIABLE

export OMP_NUM_THREADS=$((${SLURM_JOB_CPUS_PER_NODE}/2))
echo "Executable ${EXECUTABLE} running on ${SLURM_JOB_CPUS_PER_NODE} cores with ${OMP_NUM_THREADS} threads"
startexe=${EXECUTABLE}
echo $startexe
exec $startexe
