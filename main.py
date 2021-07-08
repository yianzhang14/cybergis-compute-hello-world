import json

print('running main...')

job = json.load(open('./job.json',))

print(job)