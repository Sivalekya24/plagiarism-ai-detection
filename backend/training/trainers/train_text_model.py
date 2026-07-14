import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.append(TRAINING_DIR)
sys.path.append(BACKEND_DIR)

import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from utils.load_dataset import DatasetLoader
from feature_extraction.text_feature_extractor import TextFeatureExtractor
from feature_extraction.feature_vector import FeatureVector

print("Loading dataset...")

dataset_path = os.path.join(
    TRAINING_DIR,
    "datasets",
    "AI_Human.csv"
)

df = DatasetLoader.load_dataset(dataset_path)

df = df.sample(
    n=50000,
    random_state=42
)

print("Extracting features...")

feature_df = TextFeatureExtractor.extract_dataframe(df)

X, y = FeatureVector.split(feature_df)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training XGBoost model...")

model = XGBClassifier(

    n_estimators=300,

    max_depth=6,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="binary:logistic",

    eval_metric="logloss",

    random_state=42,

    n_jobs=-1

)

model.fit(
    X_train,
    y_train
)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nAccuracy")

print(round(accuracy, 4))

print("\nClassification Report")

print(
    classification_report(
        y_test,
        predictions
    )
)

print("\n==============================")
print("Feature Importance")
print("==============================")

importance = model.feature_importances_

for feature, score in sorted(
    zip(X.columns, importance),
    key=lambda x: x[1],
    reverse=True
):
    print(f"{feature:30} {score:.4f}")


model_dir = os.path.join(
    TRAINING_DIR,
    "models"
)

os.makedirs(
    model_dir,
    exist_ok=True
)

joblib.dump(
    model,
    os.path.join(
        model_dir,
        "text_model.pkl"
    )
)

print("\nModel Saved")