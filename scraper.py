import os
import re
import requests

# 🔑 Secrets থেকে API Key পড়া
api_key = os.environ.get("SERPER_API_KEY")
url = "https://google.serper.dev/search"

# 🔍 WhatsApp ও Messenger কেন্দ্রিক সার্চ কুয়েরি
payload = {'q': 'hobby shop bangladesh "whatsapp" OR "messenger" OR "m.me"'}

headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

# 📤 API-তে রিকোয়েস্ট পাঠানো
response = requests.post(url, headers=headers, json=payload)
data = response.json()

# 📜 রেজাল্ট পার্সিং এবং ডাটা ফিল্টারিং
for item in data.get("organic", []):
  title = item.get("title")
  link = item.get("link", "")
  snippet = item.get("snippet", "")

  # 📱 বাংলাদেশের ফোন/WhatsApp নম্বর খোঁজার Regex (যেমন: 017... বা +88017...)
  phone_match = re.search(r"(\+?8801\d{9}|01\d{9})", snippet)
  phone = phone_match.group(0) if phone_match else "নম্বর পাওয়া যায়নি ❌"

  # 💬 Messenger বা Facebook লিংক শনাক্ত করা
  is_messenger = "m.me" in link or "facebook.com" in link

  print(f"📌 Shop: {title}")
  print(f"🔗 Link: {link}")
  print(f"📱 Phone/WhatsApp: {phone}")
  print(f"💬 Messenger/FB: {'হ্যাঁ 🟢' if is_messenger else 'না 🔴'}")
  print("-" * 40)
