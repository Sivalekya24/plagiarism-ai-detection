from utils.load_dataset import DatasetLoader

df = DatasetLoader.load_dataset("datasets/AI_Human.csv")   # use your actual filename

print(df["generated"].value_counts())

print("\n========== HUMAN SAMPLE ==========")
print(df[df["generated"] == 0]["text"].iloc[0][:600])

print("\n========== AI SAMPLE ==========")
print(df[df["generated"] == 1]["text"].iloc[0][:600])