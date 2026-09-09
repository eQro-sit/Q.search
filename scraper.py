import os
import re
import requests

# 🔑 Secrets থেকে API Key গ্রহণ
api_key = os.environ.get("SERPER_API_KEY")
url = "https://google.serper.dev/search"

# 🔍 হোয়াটসঅ্যাপ, মেসেঞ্জার ও বাংলা মোবাইল নম্বর কেন্দ্রিক সার্চ কুয়েরি
payload = {
    "q": 'hobby shop bangladesh ("whatsapp" OR "messenger" OR "m.me" OR "017" OR "018" OR "019" OR "016")'
}

headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

# 📤 API রিকোয়েস্ট পাঠানো
response = requests.post(url, headers=headers, json=payload)
data = response.json()

# 📜 রেজাল্ট পার্স করে ফোন ও মেসেঞ্জার এক্সট্র্যাক্ট করা
for item in data.get("organic", []):
  title = item.get("title")
  link = item.get("link", "")
  snippet = item.get("snippet", "")

  # 📱 স্পেস ও হাইফেনসহ ১১ ডিজিটের মোবাইল নম্বর খোঁজার Regex
  phone_match = re.search(
      r"(\+?880[\s\-]?1[3-9]\d{2}[\s\-]?\d{6}|01[3-9][\s\-]?\d{2}[\s\-]?\d{6}|01[3-9]\d{8})",
      snippet,
  )
  phone = phone_match.group(0) if phone_match else "নম্বর পাওয়া যায়নি ❌"

  # 💬 Messenger/Facebook শনাক্ত করা
  is_messenger = (
      "m.me" in link
      or "facebook.com" in link
      or "m.me" in snippet
      or "facebook.com" in snippet
  )

  print(f"📌 Shop: {title}")
  print(f"🔗 Link: {link}")
  print(f"📱 Phone/WhatsApp: {phone}")
  print(f"💬 Messenger/FB: {'হ্যাঁ 🟢' if is_messenger else 'না 🔴'}")
  print("-" * 40)
