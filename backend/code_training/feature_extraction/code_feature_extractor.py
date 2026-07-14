import os
import sys
import pandas as pd
from tqdm import tqdm

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_TRAINING_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

sys.path.append(CODE_TRAINING_DIR)
sys.path.append(BACKEND_DIR)

from ai_detection.algorithms.code_features import CodeFeatures


LANGUAGE_MAP = {

    "Python": 0,
    "Java": 1,
    "JavaScript": 2,
    "C": 3,
    "C++": 4,
    "C#": 5,
    "Go": 6,
    "PHP": 7,
    "Rust": 8

}


class CodeFeatureExtractor:

    @staticmethod
    def extract_dataframe(df):

        print("Extracting code features...")

        feature_rows = []

        for _, row in tqdm(df.iterrows(), total=len(df)):

            features = CodeFeatures.extract(
                row["Code"]
            )

            features["language"] = LANGUAGE_MAP.get(
                row["Language"],
                -1
            )

            features["Label"] = row["Label"]

            feature_rows.append(features)

        return pd.DataFrame(feature_rows)