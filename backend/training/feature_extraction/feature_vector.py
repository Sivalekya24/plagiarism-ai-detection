import pandas as pd


class FeatureVector:

    @staticmethod
    def split(df):

        X = df.drop(columns=["label"])

        y = df["label"]

        return X, y