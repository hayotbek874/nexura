# NEXURA: Autonomous Cyber-Intelligence & Countermeasure System

NEXURA — bu 24/7 rejimida dunyodagi kiber-tahdidlarni mustaqil o'rganuvchi, ularni AI yordamida tahlil qiluvchi va aniqlangan xavflarga qarshi texnik himoya choralarini (Countermeasures) ishlab chiquvchi avtonom platforma.

---

## 1. Asosiy Texnologiyalar va Parametrlar

Dastur quyidagi zamonaviy texnologiyalar asosida qurilgan:

- **AI Engine:**
  - **Google Gemini (1.5 Flash):** Har bir yangi tahdidni chuqur tahlil qilish, uning ishlash metodikasini (TTP) tushunish va himoya kodlarini generatsiya qilish uchun asosiy intellekt.

- **Backend Framework:**
  - **Python 3.10:** Dasturning asosiy tili.
  - **FastAPI & Uvicorn:** Hugging Face-da monitoring Dashboardini taqdim etish uchun yuqori tezlikdagi web-server.

- **Data Science & Machine Learning:**
  - **Pandas:** Ma'lumotlarni qayta ishlash va `csv` formatida saqlash.
  - **Scikit-learn:** `auto_train.py` orqali AI modellarini o'qitish va yangilash.
  - **Joblib:** Tayyor modellarni `.pkl` formatida saqlash.

- **Bulutli Infratuzilma (Cloud Infrastructure):**
  - **Hugging Face Spaces (Docker):** Dasturning 24/7 ishlashini ta'minlovchi server.
  - **Hugging Face Datasets:** O'rganilgan barcha "bilimlar" (`cyber_intel_structured.csv`) uchun bulutli ombor.

- **Data Harvesting (Ma'lumot yig'ish):**
  - **Kaggle API:** Kiberxavfsizlikka oid yirik `.csv` datasetlarni avtomatik yuklash.
  - **Hugging Face Hub API:** Boshqa ochiq kiber-datasetlarni qidirish.
  - **Feedparser & BeautifulSoup:** RSS va Atom lentalaridan (CVE, Exploit-DB) real-vaqt ma'lumotlarini olish.

## 2. Asosiy Funksional Imkoniyatlar

- **WILD DOG MODE (Autonomous Predator):** Dasturning asosiy ish rejimi. U inson aralashuvisiz cheksiz siklda ishlaydi, o'rganadi va o'zini-o'zi yangilaydi.
- **Multi-Source Intelligence:** Bir vaqtning o'zida **15 dan ortiq** global manbadan ma'lumot yig'adi:
  - **Zaifliklar:** NVD (CVE), CISA, Exploit-DB, Packet Storm, GitHub Advisories.
  - **Malware:** MalwareBazaar (abuse.ch).
  - **Yangiliklar:** The Hacker News, BleepingComputer.
  - **TTPs:** MITRE ATT&CK.
- **AI-Generated Countermeasures:** Har bir yangi topilgan tahdid uchun Gemini orqali aniq **himoya kodi (Python, Bash)** yoki **konfiguratsiya (Firewall rule)** ishlab chiqadi.
- **Incremental Learning:** `auto_train.py` moduli har safar barcha ma'lumotlarni emas, balki faqat yangi qo'shilgan bilimlarni o'rgatadi, bu esa o'qitish vaqtini bir necha daqiqadan bir necha soniyaga qisqartiradi.
- **Cloud Sync & Persistence:** O'rganilgan barcha bilimlar `cyber_intel_structured.csv` fayliga saqlanadi va darhol Hugging Face Dataset-ga yuklanadi, bu esa ma'lumotlar yo'qolishining oldini oladi.

## 3. Datasetlar va Modellar

- **Asosiy Bilimlar Bazasi:** `cyber_intel_structured.csv` — Dasturning asosiy "miyasi". Unda har bir tahdid 5 ta parametr bilan saqlanadi: `timestamp`, `attack_type`, `description`, `countermeasure`, `label`.
- **Yirik Datasetlar:** Dastur Kaggle orqali quyidagi kabi mavzularda **10 GB dan ortiq** hajmdagi `.csv` fayllarni yuklay oladi va ular asosida `auto_train.py` 40 dan ortiq individual modellarni (`.pkl`) yaratadi:
  - DDoS & Botnet Traffic
  - SQL Injection & XSS Payloads
  - Malware API Call Sequences
  - Phishing URLs and Emails
  - Network Intrusion (IDS/IPS)

## 4. Loyiha Tuzilmasi va Fayllar

- `Dockerfile`: Hugging Face-da dasturni ishga tushirish uchun konfiguratsiya.
- `requirements.txt`: Barcha zaruriy Python kutubxonalari ro'yxati.
- `backend/cyber_intel.py`: Dasturning asosiy mantig'i, "Wild Dog Mode" va barcha razvedka funksiyalari joylashgan fayl.
- `backend/main.py`: Hugging Face-da natijalarni ko'rsatib turuvchi Dashboard (FastAPI orqali).
- `backend/auto_train.py`: Yangi bilimlarni AI modellariga o'rgatuvchi skript.
- `backend/cyber_intel_structured.csv`: Dasturning o'rgangan bilimlar bazasi.

## 5. Hugging Face-ga Joylashtirish (Deployment)

1.  **Space yaratish:** Hugging Face-da yangi Space ochiladi va SDK sifatida **Docker** tanlanadi.
2.  **Secrets (Kalitlar) qo'shish:** `Settings > Variables and secrets` bo'limiga quyidagilar qo'shiladi:
    - `GEMINI_API_KEY`
    - `HF_TOKEN` (yozish huquqi bilan)
    - `HF_DATASET_REPO` (masalan, `hayotbek01/NEXURA`)
    - `KAGGLE_USERNAME` & `KAGGLE_KEY`
    - `IS_CLOUD` (qiymati `true`)
3.  **Fayllarni yuklash:** Yuqorida sanab o'tilgan barcha fayllar (`dist/` va `__pycache__/` papkalarisiz) yuklanadi.

Dastur avtomatik ravishda yig'iladi (build) va 24/7 ishlay boshlaydi.
