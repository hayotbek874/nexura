import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import os
import time

def train_sqli():
    dataset_path = 'sqli.csv'

    if not os.path.exists(dataset_path):
        print(f"!!! XATOLIK: {dataset_path} topilmadi!")
        return

    print("\n" + "="*50)
    print("   NEXURA AI: SQL INJECTION MODEL TRAINING")
    print("="*50)

    print("[1/5] Ma'lumotlar bazasi yuklanmoqda...")
    start_time = time.time()

    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(dataset_path, encoding=enc)
            print(f"      ✓ Yuklandi ({enc})")
            break
        except: continue

    if df is None:
        print("!!! XATOLIK: Encoding muammosi.")
        return

    print(f"[2/5] Ma'lumotlarni tozalash (Hajm: {len(df)} qator)...")
    df = df.dropna()
    X = df.iloc[:, 0].astype(str)
    y = df.iloc[:, 1]

    print("[3/5] Matnlarni raqamlarga o'tkazish (TF-IDF Vectorization)...")
    print("      (Bu jarayon bir oz vaqt olishi mumkin...)")
    vectorizer = TfidfVectorizer(min_df=2, max_df=0.8)
    X_vec = vectorizer.fit_transform(X)

    print("[4/5] Model o'qitilmoqda (Logistic Regression)...")
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000, verbose=1) # Verbose=1 progressni ko'rsatadi
    model.fit(X_train, y_train)

    print("[5/5] Modelni tekshirish va saqlash...")
    accuracy = model.score(X_test, y_test)

    # Saqlash
    joblib.dump(model, 'sqli_model.pkl')
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*50)
    print(f"   MUVAFFAQIYATLI: O'qitish yakunlandi!")
    print(f"   ANIQLIK DARAJASI: {accuracy * 100:.2f}%")
    print(f"   KETGAN VAQT: {duration:.2f} sekund")
    print("="*50 + "\n")

if __name__ == "__main__":
    train_sqli()
