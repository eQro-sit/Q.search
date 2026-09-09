import csv
import json
import os
import re
import requests

api_key = os.environ.get("SERPER_API_KEY")
url = "https://google.serper.dev/search"
webhook_url = "https://webhook.site/dbc228ec-f219-4692-abec-d20a9307b391" 

with open("categories.json", "r", encoding="utf-8") as f:
  categories = json.load(f)

csv_filename = "sellers.csv"
existing_links = set()

if os.path.exists(csv_filename):
  with open(csv_filename, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
      if len(row) > 5:
        existing_links.add(row[5])

print(f"🚀 স্ক্র্যাপিং শুরু... আগে থেকে {len(existing_links)} টি ডাটা সেভ করা আছে।\n")

# 📦 ১. ওয়েবহুকে পাঠানোর জন্য ব্যাচ লিস্ট ও ব্যাচ সাইজ নির্ধারণ
all_webhook_data = []
BATCH_SIZE = 50

with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
  writer = csv.writer(file)
  
  if len(existing_links) == 0:
    writer.writerow(["Category", "Keyword", "Shop Title", "Phone/WhatsApp", "Platform Type", "Link"])

  for category_name, keywords in categories.items():
    for keyword in keywords:
      for page_num in range(1, 4): 
        query = f'site:facebook.com {keyword} "whatsapp"'
        payload = {"q": query, "page": page_num}
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

        try:
          response = requests.post(url, headers=headers, json=payload)
          response.raise_for_status()
          data = response.json()

          for item in data.get("organic", []):
            link = item.get("link", "")
            
            if link in existing_links:
              continue

            title = item.get("title", "No Title")
            snippet = item.get("snippet", "")

            phone_match = re.search(
                r"(\+?880[\s\-]?1[3-9]\d{2}[\s\-]?\d{6}|01[3-9][\s\-]?\d{2}[\s\-]?\d{6}|01[3-9]\d{8})",
                snippet,
            )
            phone = phone_match.group(0) if phone_match else "N/A"

            if "facebook.com" in link or "m.me" in link:
              platform = "Small/Medium Seller (Social Only) 🟢"
            else:
              platform = "Brand / Custom Website 🌐"

            writer.writerow([category_name, keyword, title, phone, platform, link])
            existing_links.add(link)
            
            webhook_payload = {
                "category": category_name,
                "keyword": keyword,
                "shop_title": title,
                "phone": phone,
                "platform_type": platform,
                "link": link
            }
            
            # 📦 ২. লিস্টে ডাটা যুক্ত করা
            all_webhook_data.append(webhook_payload)

            # ৫০টি ডাটা পূর্ণ হলে ওয়েবহুকে পাঠানো হবে
            if len(all_webhook_data) == BATCH_SIZE:
              print(f"📤 ৫০টি ডাটার একটি ব্যাচ ওয়েবহুকে পাঠানো হচ্ছে...")
              try:
                webhook_response = requests.post(webhook_url, json=all_webhook_data)
                print(f"✅ ব্যাচ সফলভাবে পাঠানো হয়েছে! (Status: {webhook_response.status_code})")
              except Exception as webhook_err:
                print(f"⚠️ Webhook-এ পাঠাতে সমস্যা: {webhook_err}")
              
              # পরবর্তী ব্যাচের জন্য লিস্টটি খালি করা
              all_webhook_data = []

        except Exception as e:
          print(f"⚠️ {keyword} (Page {page_num}) সার্চে সমস্যা: {e}")

print(f"\n✅ নতুন ডাটা সফলভাবে {csv_filename} ফাইলে যুক্ত হয়েছে!")

# 🚀 ৩. লুপ শেষ হওয়ার পর অবশিষ্ট (৫০টির কম) ডাটা থাকলে তা ওয়েবহুকে পাঠানো
if all_webhook_data:
    print(f"\n📤 অবশিষ্ট {len(all_webhook_data)} টি নতুন ডাটা ওয়েবহুকে পাঠানো হচ্ছে...")
    try:
        webhook_response = requests.post(webhook_url, json=all_webhook_data)
        print(f"✅ Webhook-এ সফলভাবে পাঠানো হয়েছে! (Status: {webhook_response.status_code})")
    except Exception as webhook_err:
        print(f"⚠️ Webhook-এ পাঠাতে সমস্যা: {webhook_err}")
else:
    print("\nℹ️ অবশিষ্টাংশে পাঠানোর মতো কোনো নতুন ডাটা নেই।")
