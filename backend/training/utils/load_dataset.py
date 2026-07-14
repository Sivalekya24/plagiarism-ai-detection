import pandas as pd


class DatasetLoader:

    REQUIRED_COLUMNS = ["text", "generated"]

    @staticmethod
    def load_dataset(path):

        df = pd.read_csv(path)

        missing = [
            column
            for column in DatasetLoader.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        df = df.dropna(subset=["text", "generated"])

        df["text"] = df["text"].astype(str)

        df["generated"] = df["generated"].astype(int)

        return df

    @staticmethod
    def dataset_info(df):

        print("\nDataset Information")
        print("-" * 40)

        print(f"Total Samples : {len(df)}")

        print(
            "\nLabel Distribution:"
        )

        print(
            df["generated"].value_counts()
        )

        print(
            "\nColumns:"
        )

        print(
            list(df.columns)
        )