import feedparser
import pandas as pd
import os
import time

# Dunyodagi eng mashhur kiber-xavfsizlik RSS manbalari
RSS_SOURCES = [
    "https://thehackernews.com/feeds/posts/default",
    "https://www.darkreading.com/rss.xml",
    "https://krebsonsecurity.com/feed/",
    "https://www.bleepingcomputer.com/feed/"
]

def fetch_cyber_news():
    print("\n" + "="*60)
    print("   NEXURA AGI: WEB-INTELLIGENCE SCANNING...")
    print("="*60)
    
    intel_data = []

    for url in RSS_SOURCES:
        try:
            print(f">>> Scanning: {url}")
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Yangilik sarlavhasi va qisqacha mazmuni
                full_text = f"{entry.title}. {entry.get('summary', '')}"
                # Label 1 - chunki bular kiber-xavf haqidagi real ma'lumotlar
                intel_data.append({"text": full_text, "label": 1})
        except Exception as e:
            print(f"!!! Error scanning {url}: {e}")

    if intel_data:
        df = pd.DataFrame(intel_data)
        file_name = "cyber_intel.csv"
        
        # Agar fayl oldindan bo'lsa, yangisini qo'shamiz (Append)
        if os.path.exists(file_name):
            df.to_csv(file_name, mode='a', header=False, index=False)
        else:
            df.to_csv(file_name, index=False)
            
        print(f"\n[ OK ] Jami {len(intel_data)} ta yangi kiber-xavf qoliplari yig'ildi.")
        print(f"[ OK ] Ma'lumotlar '{file_name}' fayliga saqlandi.")
        return True
    else:
        print(">>> Hech qanday yangi ma'lumot topilmadi.")
        return False

if __name__ == "__main__":
    if fetch_cyber_news():
        print("\nAI endi o'rganishni boshlashi mumkin.")
        # Avtomatik o'qitishni boshlash uchun:
        # os.system("python auto_train.py")
