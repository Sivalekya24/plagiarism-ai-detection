import os

from Utils.load_code_dataset import CodeDatasetLoader


dataset_folder = "datasets"

df = CodeDatasetLoader.load_dataset(
    dataset_folder
)

CodeDatasetLoader.dataset_info(df)

print("\n")

balanced = CodeDatasetLoader.sample_dataset(
    df,
    samples=50000
)

print("=" * 60)
print("Balanced Dataset")
print("=" * 60)

print(
    balanced["Label"].value_counts()
)

print("\n")

print("=" * 60)
print("First Sample")
print("=" * 60)

print(
    balanced.iloc[0]
)

print("\n")

print("=" * 60)
print("First Code")
print("=" * 60)

print(
    balanced.iloc[0]["Code"][:1000]
)