#!/bin/bash

#SBATCH --job-name=sim_1        # job name (default is the name of this file)
#SBATCH --output=log.%x.job_%j  # file name for stdout/stderr (%x will be replaced with the job name, %j with the jobid)
#SBATCH --time=1:00:00          # maximum wall time allocated for the job (D-H:MM:SS)
#SBATCH --partition=gpXY        # put the job into the gpu partition
#SBATCH --exclusive             # request exclusive allocation of resources
#SBATCH --mem=20G               # RAM per node
#SBATCH --threads-per-core=1    # do not use hyperthreads (i.e. CPUs = physical cores below)
#SBATCH --cpus-per-task=4       # number of CPUs per process

## nodes allocation
#SBATCH --nodes=2               # number of nodes
#SBATCH --ntasks-per-node=2     # MPI processes per node

## GPU allocation - variant A
#SBATCH --gres=gpu:2            # number of GPUs per node (gres=gpu:N)

## GPU allocation - variant B
## #SBATCH --gpus-per-task=1       # number of GPUs per process
## #SBATCH --gpu-bind=single:1     # bind each process to its own GPU (single:<tasks_per_gpu>)

# start the job in the directory it was submitted from
cd "$SLURM_SUBMIT_DIR"

# program execution - variant 1
mpirun ./sim

# program execution - variant 2
#srun ./sim