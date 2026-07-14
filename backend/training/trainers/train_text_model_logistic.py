import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

sys.path.append(TRAINING_DIR)
sys.path.append(BACKEND_DIR)

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
from sklearn.calibration import CalibratedClassifierCV
from utils.load_dataset import DatasetLoader
from feature_extraction.text_feature_extractor import TextFeatureExtractor
from feature_extraction.feature_vector import FeatureVector


DATASET = "datasets/AI_Human.csv"


print("Loading dataset...")

df = DatasetLoader.load_dataset(DATASET)

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

base_model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

classifier = CalibratedClassifierCV(
    estimator=base_model,
    method="sigmoid",
    cv=5
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", classifier)
])

print("Training model...")

pipeline.fit(X_train, y_train)

classifier = pipeline.named_steps["classifier"]

# Get the calibrated logistic regression model
base_estimator = classifier.calibrated_classifiers_[0].estimator

coefficients = base_estimator.coef_[0]

feature_names = X.columns

print("\n==============================")
print("Feature Importance")
print("==============================")

for feature, coef in sorted(
    zip(feature_names, coefficients),
    key=lambda x: abs(x[1]),
    reverse=True
):
    print(f"{feature:30} {coef:.4f}")

predictions = pipeline.predict(X_test)

print("\nAccuracy")

print(
    accuracy_score(
        y_test,
        predictions
    )
)

print("\nClassification Report")

print(
    classification_report(
        y_test,
        predictions
    )
)

joblib.dump(
    pipeline,
    "models/text_model.pkl"
)

print("\nModel Saved")