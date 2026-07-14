import os
import sys
import joblib

from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_TRAINING_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

sys.path.append(CODE_TRAINING_DIR)
sys.path.append(BACKEND_DIR)

from Utils.load_code_dataset import CodeDatasetLoader
from feature_extraction.code_feature_extractor import CodeFeatureExtractor
from feature_extraction.code_feature_vector import CodeFeatureVector


print("Loading Dataset...")

dataset_folder = os.path.abspath(
    os.path.join(
        CODE_TRAINING_DIR,
        "datasets"
    )
)

print(dataset_folder)

df = CodeDatasetLoader.load_dataset(
    dataset_folder
)

print("\nCreating Balanced Dataset...")

df = CodeDatasetLoader.sample_dataset(
    df,
    samples=100000,
    random_state=42
)

print(df["Label"].value_counts())

print("\nExtracting Features...")

feature_df = CodeFeatureExtractor.extract_dataframe(df)

X, y = CodeFeatureVector.split(feature_df)

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)

print("\nTraining XGBoost...")

model = XGBClassifier(

    n_estimators=300,

    max_depth=7,

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

print("\n==============================")

print("Accuracy")

print("==============================")

print(round(accuracy,4))

print("\n==============================")

print("Classification Report")

print("==============================")

print(

    classification_report(

        y_test,

        predictions

    )

)

print("\n==============================")

print("Confusion Matrix")

print("==============================")

print(

    confusion_matrix(

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

    print(

        f"{feature:35} {score:.4f}"

    )

model_dir = os.path.abspath(

    os.path.join(

        CODE_TRAINING_DIR,

        "models"

    )

)

os.makedirs(

    model_dir,

    exist_ok=True

)

model_path = os.path.join(

    model_dir,

    "code_model.pkl"

)

joblib.dump(

    model,

    model_path

)

print("\nModel Saved Successfully")

print(model_path)