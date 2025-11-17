import joblib
from sklearn.ensemble import RandomForestClassifier
from .preprocess import preprocess

def train_model(df):
    X_scaled, y, scaler, label_enc = preprocess(df)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    joblib.dump(model, 'src/model.pkl')
    joblib.dump(scaler, 'src/scaler.pkl')
    joblib.dump(label_enc, 'src/label_enc.pkl')

def predict_single(df):
    model = joblib.load('src/model.pkl')
    scaler = joblib.load('src/scaler.pkl')
    label_enc = joblib.load('src/label_enc.pkl')
    df = df.copy()
    df['genre'] = label_enc.transform(df['genre'])
    df = df.drop(['movie_id', 'title'], axis=1)
    X = scaler.transform(df.drop('box_office_hit', axis=1))
    df['prediction'] = model.predict(X)
    return df[['prediction']]