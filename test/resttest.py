import requests, json

response = requests.get('https://10.10.10.51/api/status')

print('Response Code:', response.status_code)

if response.status_code == 200:
    data = response.json()
    print(data['serviceName'], data['version'], data['uptime'])

body = {'username':'test','password':'test','deviceName':'test'}
headers = {'Content-type':'application/json', 'Accept':'application/json'}

print(body)
print(headers)

response = requests.post(url='https://10.10.10.51/api/login', json=body) #, headers=headers)

print('Response Code:', response.status_code)

if response.status_code == 200:
    print(response.json())

