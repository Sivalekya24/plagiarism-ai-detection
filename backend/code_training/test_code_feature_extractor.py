import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_TRAINING_DIR = CURRENT_DIR
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

sys.path.append(CODE_TRAINING_DIR)
sys.path.append(BACKEND_DIR)

from Utils.load_code_dataset import CodeDatasetLoader
from feature_extraction.code_feature_extractor import CodeFeatureExtractor


dataset_folder = "datasets"

df = CodeDatasetLoader.load_dataset(
    dataset_folder
)

# Use only 20 samples for testing
df = df.sample(
    n=20,
    random_state=42
)

feature_df = CodeFeatureExtractor.extract_dataframe(df)

print()

print(feature_df.head())

print()

print(feature_df.columns)