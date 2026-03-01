import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import time

def train_phishing():
    # Siz yuklagan aniq fayl nomi
    dataset_path = 'phishing_email.csv'

    if not os.path.exists(dataset_path):
        print(f"!!! XATOLIK: {dataset_path} topilmadi! Backend papkasini tekshiring.")
        return

    print("\n" + "="*60)
    print("   NEXURA AI: ADVANCED PHISHING DETECTION TRAINING")
    print("="*60)

    print("[1/5] Katta hajmdagi dataset yuklanmoqda (104MB)...")
    start_time = time.time()

    # Katta fayllar uchun optimallashgan o'qish
    try:
        df = pd.read_csv(dataset_path)
        print("      ✓ Dataset muvaffaqiyatli o'qildi.")
    except Exception as e:
        print(f"!!! XATOLIK: Faylni o'qib bo'lmadi: {e}")
        return

    # Ustun nomlarini aniqlaymiz
    print(f"      Mavjud ustunlar: {df.columns.tolist()}")

    # Odatda phishing datasetlarda: 1-ustun matn, oxirgi ustun label
    # Agar ustun nomlari boshqacha bo'lsa, avtomatik moslashamiz
    text_col = df.columns[0]
    label_col = df.columns[-1]

    print(f"[2/5] Ma'lumotlarni tozalash...")
    df = df.dropna()
    X = df[text_col].astype(str)
    y = df[label_col]

    print("[3/5] NLP Analiz: TF-IDF Vectorization boshlandi...")
    # Max_features ni 5000 qilib cheklaymiz (tezlik va xotira uchun)
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1,2))
    X_vec = vectorizer.fit_transform(X)

    print("[4/5] Model o'qitilmoqda (Bu bir oz vaqt olishi mumkin)...")
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

    # Random Forest - phishing uchun juda kuchli algoritm
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1, verbose=1)
    model.fit(X_train, y_train)

    print("[5/5] Model aniqligini tekshirish...")
    accuracy = model.score(X_test, y_test)

    # Modellarni saqlash
    joblib.dump(model, 'phishing_model.pkl')
    joblib.dump(vectorizer, 'phishing_vectorizer.pkl')

    end_time = time.time()
    print("\n" + "="*60)
    print(f"   TABRIKLAYMIZ: NEXURA Phishing modeli tayyor!")
    print(f"   ANIQLIK: {accuracy * 100:.2f}%")
    print(f"   KETGAN VAQT: {end_time - start_time:.2f} sekund")
    print("   MODEL FAYLI: phishing_model.pkl")
    print("="*60 + "\n")

if __name__ == "__main__":
    train_phishing()
