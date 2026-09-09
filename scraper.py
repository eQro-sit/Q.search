import csv
import os
import re
import requests

api_key = os.environ.get("SERPER_API_KEY")
url = "https://google.serper.dev/search"

# 🔍 মিক্সড সার্চ: একটি শুধু ফেসবুকের জন্য, আরেকটি সাধারণ (যেখানে ওয়েবসাইটও আসবে)
search_terms = [
    {"category": "Aquarium (FB Only) 🐟", "query": 'site:facebook.com ("guppy" OR "kom damer mach" OR "aquarium") "whatsapp"'},
    {"category": "Plant (Mixed) 🌿", "query": '("bideshi gach" OR "ucco folonshil" OR "nursery") "whatsapp" -pinterest'}
]

headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
csv_filename = "sellers.csv"

print("🚀 ডাটা স্ক্র্যাপিং শুরু হচ্ছে...\n")

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
  writer = csv.writer(file)
  writer.writerow(["Category", "Shop Title", "Phone/WhatsApp", "Platform Type", "Link"])

  for term in search_terms:
    category_name = term["category"]
    payload = {"q": term["query"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # API তে কোনো এরর থাকলে তা ধরবে
        data = response.json()
        
        for item in data.get("organic", []):
          title = item.get("title", "No Title")
          link = item.get("link", "")
          snippet = item.get("snippet", "")

          # 📱 ফোন নম্বর শনাক্ত করার Regex
          phone_match = re.search(
              r"(\+?880[\s\-]?1[3-9]\d{2}[\s\-]?\d{6}|01[3-9][\s\-]?\d{2}[\s\-]?\d{6}|01[3-9]\d{8})",
              snippet,
          )
          phone = phone_match.group(0) if phone_match else "N/A"

          # 🌐 প্লাটফর্ম টাইপ নির্ধারণ
          if "facebook.com" in link or "m.me" in link:
            platform = "Small Seller (Social Only) 🟢"
          else:
            platform = "Brand / Custom Website 🌐"

          # 💾 CSV ফাইলে সেভ করা
          writer.writerow([category_name, title, phone, platform, link])
          
    except Exception as e:
        print(f"⚠️ {category_name} সার্চ করার সময় সমস্যা হয়েছে: {e}")

print(f"✅ সফলভাবে সকল ডাটা {csv_filename} ফাইলে সেভ হয়েছে!")
