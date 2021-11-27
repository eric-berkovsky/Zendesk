import requests
from config import credentials, subdomain

payload = {
    'query': 'type:ticket status:open',
    'sort_by': 'created_at',
    'sort_order': 'asc'
}

session = requests.Session()
session.auth = credentials
url = f'https://{subdomain}.zendesk.com/api/v2/search.json?'

response = session.get(url, params=payload)
data = response.json()['results']
for i in range(5):
    print(data[i]['subject'])
