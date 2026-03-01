import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import time

def train_xss():
    dataset_path = 'xss.csv'

    if not os.path.exists(dataset_path):
        print(f"!!! XATOLIK: {dataset_path} topilmadi! Iltimos datasetni backend papkasiga joylang.")
        return

    print("\n" + "="*60)
    print("   NEXURA AI: XSS (CROSS-SITE SCRIPTING) DETECTION TRAINING")
    print("="*60)

    print("[1/5] XSS dataset yuklanmoqda...")
    start_time = time.time()

    # Datasetni o'qiymiz
    try:
        df = pd.read_csv(dataset_path)
        print("      ✓ Dataset yuklandi.")
    except:
        df = pd.read_csv(dataset_path, encoding='latin-1')

    # Ustunlarni aniqlaymiz (Odatda 'Sentence' va 'Label')
    text_col = df.columns[0]
    label_col = df.columns[-1]

    print(f"[2/5] Ma'lumotlarni tozalash (Hajm: {len(df)} qator)...")
    df = df.dropna()
    X = df[text_col].astype(str)
    y = df[label_col]

    print("[3/5] Matnlarni vektorlash (TF-IDF Vectorization)...")
    # XSS uchun maxsus belgilar (<, >, /) juda muhim, shuning uchun char-level tahlil qilamiz
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 4), max_features=10000)
    X_vec = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

    print("[4/5] Model o'qitilmoqda (Random Forest)...")
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1, verbose=1)
    model.fit(X_train, y_train)

    print("[5/5] Model aniqligini tekshirish...")
    accuracy = model.score(X_test, y_test)

    # Saqlash
    joblib.dump(model, 'xss_model.pkl')
    joblib.dump(vectorizer, 'xss_vectorizer.pkl')

    end_time = time.time()
    print("\n" + "="*60)
    print(f"   TABRIKLAYMIZ: XSS mudofaa modeli tayyor!")
    print(f"   ANIQLIK: {accuracy * 100:.2f}%")
    print(f"   MODEL FAYLI: xss_model.pkl")
    print("="*60 + "\n")

if __name__ == "__main__":
    train_xss()
