
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--lag', default=500)
parser.add_argument('--dest', default='run.sh')
parser.add_argument('--msm', default=False, action='store_true')
args = parser.parse_args()
print(args)

template = """#!/bin/bash

#SBATCH --job-name=best_f_{lag}
#SBATCH -D /home/marscher/NO_BACKUP/msm_lag_{lag}
#SBATCH --output=logs/best_feat%A_%a.out
#SBATCH --time=1-0
#SBATCH --mem=250000M
#SBATCH --cpus-per-task=24
#SBATCH --partition=big
#SBATCH --array 0-167
#SBATCH --export=PYTHONUNBUFFERED=1
#SBATCH --mail-type=fail
#SBATCH --mail-user=m.scherer@fu-berlin.de

export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE
/home/marscher/miniconda3/envs/cov_/bin/python /home/marscher/feature_sel/analysis/{script} \
   --output=/home/marscher/NO_BACKUP/final_lag_{lag} --lag={lag} $SLURM_ARRAY_TASK_ID
""".format(lag=args.lag,
           script='calc_cov_best_contacts_torsions.py' if not args.msm else 'msm.py',
           )

with open(args.dest, 'w') as f:
    f.write(template)
