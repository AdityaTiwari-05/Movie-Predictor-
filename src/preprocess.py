import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def preprocess(df):
    df = df.copy()
    df = df.drop(['movie_id', 'title'], axis=1)

    label_enc = LabelEncoder()
    df['genre'] = label_enc.fit_transform(df['genre'])

    X = df.drop('box_office_hit', axis=1)
    y = df['box_office_hit']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, label_enc