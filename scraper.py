import csv
import json
import os
import re
import requests

api_key = os.environ.get("SERPER_API_KEY")
url = "https://google.serper.dev/search"

# 📂 categories.json ফাইল থেকে ডাটা লোড করা
with open("categories.json", "r", encoding="utf-8") as f:
  categories = json.load(f)

csv_filename = "sellers.csv"
print("🚀 ডাটা স্ক্র্যাপিং শুরু হচ্ছে...\n")

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
  writer = csv.writer(file)
  writer.writerow(
      ["Category", "Keyword", "Shop Title", "Phone/WhatsApp", "Platform Type", "Link"]
  )

  # 🔄 ক্যাটাগরি এবং কিউওয়ার্ডের লুপ
  for category_name, keywords in categories.items():
    for keyword in keywords:
      # 🔍 ফ্লেক্সিবল সার্চ কুয়েরি তৈরি
      query = f'site:facebook.com {keyword} "whatsapp"'
      payload = {"q": query}
      headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

      try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        for item in data.get("organic", []):
          title = item.get("title", "No Title")
          link = item.get("link", "")
          snippet = item.get("snippet", "")

          # 📱 ফোন নম্বর শনাক্তকরণ
          phone_match = re.search(
              r"(\+?880[\s\-]?1[3-9]\d{2}[\s\-]?\d{6}|01[3-9][\s\-]?\d{2}[\s\-]?\d{6}|01[3-9]\d{8})",
              snippet,
          )
          phone = phone_match.group(0) if phone_match else "N/A"

          # 🌐 প্লাটফর্ম টাইপ
          if "facebook.com" in link or "m.me" in link:
            platform = "Small Seller (Social Only) 🟢"
          else:
            platform = "Brand / Custom Website 🌐"

          writer.writerow(
              [category_name, keyword, title, phone, platform, link]
          )

      except Exception as e:
        print(f"⚠️ {keyword} সার্চ করার সময় সমস্যা হয়েছে: {e}")

print(f"\n✅ সকল ডাটা সফলভাবে {csv_filename} ফাইলে সেভ হয়েছে!")
