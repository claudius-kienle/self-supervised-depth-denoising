#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=privat@claudiuskienle.de
#SBATCH --partition=gpu_4,gpu_8
#SBATCH --nodes=1
#SBATCH --cpus-per-task=40
#SBATCH --time=24:00:00
#SBATCH --mem=20000mb   
#SBATCH --gres=gpu:2
#SBATCH --export=ALL,EXECUTABLE="python ../../../src/trainers/trainer.py --epochs=500 --batch_size=17 --save=True --dataset_path=../../../resources/images/calibrated/3d_aligned --dir_checkpoint=../../../resources/models/calibrated/3d_aligned_cropped"
#SBATCH --output="train_models_calibrated_cropped.out"
#SBATCH -J TrainUNet

#Usually you should set
export KMP_AFFINITY=compact,1,0
#export KMP_AFFINITY=verbose,compact,1,0 prints messages concerning the supported affinity
#KMP_AFFINITY Description: https://software.intel.com/en-us/node/524790#KMP_AFFINITY_ENVIRONMENT_VARIABLE

export OMP_NUM_THREADS=$((${SLURM_JOB_CPUS_PER_NODE}/2))
echo "Executable ${EXECUTABLE} running on ${SLURM_JOB_CPUS_PER_NODE} cores with ${OMP_NUM_THREADS} threads"
startexe=${EXECUTABLE}
echo $startexe
exec $startexe
