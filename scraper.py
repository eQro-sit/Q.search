import os
import requests
import json

# GitHub Secrets থেকে সিক্রেট এপিআই কী পড়া
api_key = os.environ.get("SERPER_API_KEY")

url = "https://google.serper.dev/search"

# আমরা যে তথ্য খুঁজতে চাই (Search Query)
payload = json.dumps({
  "q": "hobby shop bangladesh phone number"
})

headers = {
  'X-API-KEY': api_key,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
