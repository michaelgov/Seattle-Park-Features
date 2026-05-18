import requests

url = "https://unveiled-freely-defacing.ngrok-free.dev/parks/1231989812"

response = requests.get(url)

print(response.json())