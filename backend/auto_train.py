import os
import pandas as pd
import joblib
import time
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

def detect_dataset_type(df):
    """Fayl matnli (NLP) yoki raqamli (Network) ekanligini aniqlaydi"""
    # Agar birinchi ustun uzun matn bo'lsa - bu NLP
    first_val = str(df.iloc[0, 0])
    if len(first_val.split()) > 3 or any(c in first_val for c in ['<', '>', '(', ')', '/', '=']):
        return "TEXT"
    return "NUMERIC"

def autonomous_train():
    print("\n" + "!"*60)
    print("   NEXURA AUTONOMOUS LEARNING HUB: STARTING SCAN...")
    print("!"*60)

    files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if not files:
        print(">>> Hech qanday dataset (.csv) topilmadi.")
        return

    for file in files:
        model_name = file.replace('.csv', '')
        pkl_path = f"{model_name}_model.pkl"
        
        # Agar model allaqachon o'qitilgan bo'lsa, tashlab o'tamiz (ixtiyoriy)
        if os.path.exists(pkl_path):
            print(f">>> [{model_name}] allaqachon o'qitilgan. Yangilanmoqda...")

        print(f"\n--- Tahlil qilinmoqda: {file} ---")
        try:
            # Encodingni aniqlash
            df = None
            for enc in ['utf-8', 'latin-1', 'utf-16']:
                try:
                    df = pd.read_csv(file, encoding=enc)
                    break
                except: continue
            
            if df is None: continue

            df = df.dropna()
            dtype = detect_dataset_type(df)
            print(f"    Turi: {dtype} | Hajmi: {len(df)} qator")

            target_col = df.columns[-1]
            X_raw = df.iloc[:, 0] if dtype == "TEXT" else df.drop(df.columns[-1], axis=1)
            y = LabelEncoder().fit_transform(df[target_col].astype(str))

            if dtype == "TEXT":
                print("    NLP o'qitish boshlandi...")
                vectorizer = TfidfVectorizer(max_features=5000)
                X = vectorizer.fit_transform(X_raw.astype(str))
                joblib.dump(vectorizer, f"{model_name}_vectorizer.pkl")
            else:
                print("    Network/Numeric o'qitish boshlandi...")
                scaler = StandardScaler()
                # Faqat raqamli ustunlarni olamiz
                X_numeric = X_raw.select_dtypes(include=['number'])
                X = scaler.fit_transform(X_numeric)
                joblib.dump(scaler, f"{model_name}_scaler.pkl")

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            
            model = RandomForestClassifier(n_estimators=50, n_jobs=-1)
            model.fit(X_train, y_train)
            
            acc = model.score(X_test, y_test)
            joblib.dump(model, pkl_path)
            
            print(f"    Muvaffaqiyat! Aniqlik: {acc*100:.2f}% | Model: {pkl_path}")

        except Exception as e:
            print(f"    Xatolik [{file}]: {e}")

    print("\n" + "!"*60)
    print("   AVTONOM O'QITISH YAKUNLANDI. BARCHA MODELLAR TAYYOR.")
    print("!"*60 + "\n")

if __name__ == "__main__":
    autonomous_train()
