import os
import sys
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

sys.path.append(TRAINING_DIR)
sys.path.append(BACKEND_DIR)

from utils.load_dataset import DatasetLoader
from feature_extraction.text_feature_extractor import TextFeatureExtractor
from feature_extraction.feature_vector import FeatureVector

DATASET = "datasets/AI_Human.csv"

print("Loading model...")

model = joblib.load("models/text_model.pkl")

print("Loading dataset...")

df = DatasetLoader.load_dataset(DATASET)

# Use a validation subset
df = df.sample(n=10000, random_state=123)

print("Extracting features...")

feature_df = TextFeatureExtractor.extract_dataframe(df)

X, y = FeatureVector.split(feature_df)

predictions = model.predict(X)

probabilities = model.predict_proba(X)[:, 1]

print("\nAccuracy")
print(accuracy_score(y, predictions))

print("\nROC AUC")
print(roc_auc_score(y, probabilities))

print("\nClassification Report")
print(classification_report(y, predictions))

cm = confusion_matrix(y, predictions)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)

disp.plot()

plt.show()