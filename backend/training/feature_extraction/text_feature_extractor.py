import os
import sys
import pandas as pd
from tqdm import tqdm

# Add backend to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.append(BACKEND_DIR)

from ai_detection.algorithms.text_features import TextFeatures


class TextFeatureExtractor:

    @staticmethod
    def extract_dataframe(df):

        features = []

        print("Extracting text features...")

        for _, row in tqdm(df.iterrows(), total=len(df)):

            feature = TextFeatures.extract(row["text"])

            feature["label"] = row["generated"]

            features.append(feature)

        return pd.DataFrame(features)