import json
import os

print('running main...\n')

print('./job.json\n')
job = json.load(open('./job.json',))

print('SLURM_NODEID\n')
print(os.environ['SLURM_NODEID'])

print('SLURM_PROCID\n')
print(os.environ['SLURM_PROCID'])

print('job_id')
print(os.environ['job_id'])

print(job)