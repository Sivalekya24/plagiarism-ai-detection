from utils.load_dataset import DatasetLoader

DATASET = "datasets/AI_Human.csv"

df = DatasetLoader.load_dataset(DATASET)

DatasetLoader.dataset_info(df)

print("\nFirst Sample\n")

print(df.iloc[0])

print("=" * 80)

print("\nSample with generated = 0\n")
print(df[df["generated"] == 0].iloc[0]["text"])

print("\n" + "=" * 80)

print("\nSample with generated = 1\n")
print(df[df["generated"] == 1].iloc[0]["text"])