import os
import pandas as pd


class CodeDatasetLoader:

    REQUIRED_COLUMNS = [
        "Code",
        "Language",
        "Label"
    ]

    LABEL_MAPPING = {

        "HUMAN_GENERATED": 0,

        "MACHINE_GENERATED": 1,

        "MACHINE_GENERATED_ADVERSARIAL": 1,

        "MACHINE_REFINED": 1

    }

    @staticmethod
    def load_dataset(folder_path):

        dataframes = []

        parquet_files = [

            "train-00000-of-00003.parquet",

            "train-00001-of-00003.parquet",

            "train-00002-of-00003.parquet"

        ]

        for file in parquet_files:

            file_path = os.path.join(
                folder_path,
                file
            )

            if not os.path.exists(file_path):

                raise FileNotFoundError(
                    f"Dataset not found : {file_path}"
                )

            df = pd.read_parquet(file_path)

            dataframes.append(df)

        df = pd.concat(
            dataframes,
            ignore_index=True
        )

        missing = [

            column

            for column in CodeDatasetLoader.REQUIRED_COLUMNS

            if column not in df.columns

        ]

        if missing:

            raise ValueError(
                f"Missing Columns : {missing}"
            )

        df = df[
            CodeDatasetLoader.REQUIRED_COLUMNS
        ].copy()

        df = df.dropna()

        df["Code"] = df["Code"].astype(str)

        df["Language"] = df["Language"].astype(str)

        df["Label"] = df["Label"].map(
            CodeDatasetLoader.LABEL_MAPPING
        )

        df = df.dropna(
            subset=["Label"]
        )

        df["Label"] = df["Label"].astype(int)

        return df

    @staticmethod
    def dataset_info(df):

        print("\nDataset Information")
        print("=" * 60)

        print(f"Total Samples : {len(df)}")

        print("\nLanguage Distribution")
        print("-" * 60)

        print(
            df["Language"].value_counts()
        )

        print("\nBinary Label Distribution")
        print("-" * 60)

        print(
            df["Label"].value_counts()
        )

        print("\nMeaning")
        print("0 -> Human Generated")
        print("1 -> AI Generated")

        print("\nColumns")
        print("-" * 60)

        print(
            list(df.columns)
        )

    @staticmethod
    def sample_dataset(
        df,
        samples=50000,
        random_state=42
    ):

        human = df[
            df["Label"] == 0
        ]

        ai = df[
            df["Label"] == 1
        ]

        human_size = samples // 2

        ai_size = samples // 2

        human = human.sample(
            n=min(
                human_size,
                len(human)
            ),
            random_state=random_state
        )

        ai = ai.sample(
            n=min(
                ai_size,
                len(ai)
            ),
            random_state=random_state
        )

        balanced = pd.concat(
            [
                human,
                ai
            ]
        )

        balanced = balanced.sample(
            frac=1,
            random_state=random_state
        ).reset_index(drop=True)

        return balanced