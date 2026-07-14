from utils.load_dataset import DatasetLoader
from feature_extraction.text_feature_extractor import TextFeatureExtractor

DATASET = "datasets/AI_Human.csv"

df = DatasetLoader.load_dataset(DATASET)

sample_df = df.sample(20, random_state=42)

feature_df = TextFeatureExtractor.extract_dataframe(sample_df)

print(feature_df.head())

print(feature_df.columns)