import json

print('running main...')

app = json.load(open('./app.json',))

print(app)