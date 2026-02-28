import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model():
    dataset_path = 'data.csv'

    if not os.path.exists(dataset_path):
        print(f"Xatolik: {dataset_path} fayli topilmadi!")
        return

    print(f"AI: '{dataset_path}' yuklanmoqda...")
    df = pd.read_csv(dataset_path)

    # Ustun nomlaridagi bo'sh joylarni olib tashlaymiz va kichik harfga o'tkazamiz
    df.columns = df.columns.str.strip().str.lower()

    print("Mavjud ustunlar:", list(df.columns))

    # 'class' ustunini qidiramiz
    target_col = None
    if 'class' in df.columns:
        target_col = 'class'
    elif 'label' in df.columns:
        target_col = 'label'
    else:
        # Agar nomi topilmasa, eng oxirgi ustunni maqsad deb olamiz
        target_col = df.columns[-1]
        print(f"Ogohlantirish: 'class' nomi topilmadi. '{target_col}' ustuni nishon sifatida olindi.")

    # Keraksiz ustunlarni o'chirish
    if 'num_outbound_cmds' in df.columns:
        df.drop('num_outbound_cmds', axis=1, inplace=True)

    # Kategorik ustunlarni (matnli) raqamlarga o'tkazish
    le_dict = {}
    # Faqat matnli (object) ustunlarni topamiz (target ustunidan tashqari)
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if target_col in categorical_cols:
        categorical_cols.remove(target_col)

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        le_dict[col] = le

    # Maqsad (target) ustunini raqamga o'tkazamiz
    le_class = LabelEncoder()
    df[target_col] = le_class.fit_transform(df[target_col].astype(str))

    X = df.drop(target_col, axis=1)
    y = df[target_col]

    print(f"AI: Ma'lumotlar tayyorlandi. O'qitish boshlanmoqda...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Modelni o'qitish
    model = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"AI: O'qitish yakunlandi! Aniqlik darajasi: {accuracy * 100:.2f}%")

    # Saqlash
    joblib.dump(model, 'nexura_ai_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(le_dict, 'label_encoders.pkl')
    joblib.dump(le_class, 'class_encoder.pkl')

    print("AI: Model va sozlamalar muvaffaqiyatli saqlandi.")

if __name__ == "__main__":
    train_model()
