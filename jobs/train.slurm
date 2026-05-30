#!/bin/bash
#SBATCH -J train              # job name
#SBATCH -o logs/train.%j.out  # stdout (the %j is the job ID)
#SBATCH -e logs/train.%j.err  # stderr
#SBATCH -p gh                 # queue: gh (GPU); use gh-dev for short test jobs
#SBATCH -N 1                  # nodes
#SBATCH -n 1                  # tasks
#SBATCH -t 02:00:00           # wall time (hh:mm:ss)
#SBATCH -A TRA25001           # workshop allocation; change to your own after the program

# Load modules and activate your environment
module load python3
source .venv/bin/activate

# Run training (reads data/processed/, writes results/)
python scripts/train_model.py
