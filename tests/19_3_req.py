import json

import requests

# # МЕТОД GET
status = 'available'

response = requests.get(f'https://petstore.swagger.io/v2/pet/findByStatus?status={status}', headers={'accept':'application/json'})

print(response.status_code)
print(response.text)
print(response.json())
print(type(response.json()))

# МЕТОД POST
data = {
  "id": 9223372036854773000,
  "category": {
    "id": 0,
    "name": "string"
  },
  "name": "doggie",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}

response1 = requests.post(f'https://petstore.swagger.io/v2/pet', headers={'accept':'application/json', 'Content-Type': 'application/json'}, json=data)
print("добавляем нового питомца, статус кода:", response1.status_code)
print(response1.text)

# МЕТОД PUT

data = {
  "id": 0,
  "category": {
    "id": 0,
    "name": "string"
  },
  "name": "doggie",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}
headers = {
    'accept': 'application/json',
'Content-Type': 'application/json'
}
res = requests.put(f'https://petstore.swagger.io/v2/pet/', headers=headers, json=data)
print("Обновляем существующего питомца, статус кода:", res.status_code)
print(res.json())

# МЕТОД DELETE
url = 'https://petstore.swagger.io/v2/pet/9223372036854773000'

headers = {
    'accept': 'application/json',
'Content-Type': 'application/json'
}

response2 = requests.delete(url, headers=headers)
# response2 = requests.delete(f'https://petstore.swagger.io/v2/pet/{petID}', headers={'accept':'application/json', 'Content-Type': 'application/json'})
print("удаляем питомца, статус кода:", response2.status_code)
print(response2.text)

