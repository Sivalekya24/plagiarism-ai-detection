import os
import time
import joblib

from ai_detection.algorithms.code_features import CodeFeatures


class CodeModelService:

    MIN_LINES = 5

    CONFIDENCE_THRESHOLD = 70.0

    MODEL_PATH = os.path.join(

        os.path.dirname(__file__),

        "..",

        "..",

        "code_training",

        "models",

        "code_model.pkl"

    )

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

    FEATURE_COLUMNS = [

        "total_lines",

        "blank_lines",

        "blank_line_ratio",

        "average_line_length",

        "max_line_length",

        "min_line_length",

        "line_length_variance",

        "empty_line_groups",

        "comment_lines",

        "single_comments",

        "block_comments",

        "docstring_comments",

        "comment_ratio",

        "identifier_count",

        "unique_identifier_count",

        "identifier_diversity",

        "average_identifier_length",

        "camel_case_count",

        "snake_case_count",

        "uppercase_identifier_count",

        "single_character_identifier_count",

        "total_tokens",

        "unique_tokens",

        "token_diversity",

        "keyword_count",

        "operator_count",

        "number_literals",

        "string_literals",

        "import_count",

        "loop_count",

        "branch_count",

        "function_keyword_count",

        "logical_operator_count",

        "function_count",

        "max_nesting_depth",

        "cyclomatic_complexity",

        "language",

        "character_entropy",

        "token_entropy"

    ]

    model = None

    @classmethod
    def load_model(cls):

        if cls.model is None:

            if not os.path.exists(cls.MODEL_PATH):

                raise FileNotFoundError(

                    cls.MODEL_PATH

                )

            cls.model = joblib.load(

                cls.MODEL_PATH

            )

    @classmethod
    def predict(

        cls,

        code,

        language

    ):

        cls.load_model()

        start = time.perf_counter()

        features = CodeFeatures.extract(

            code

        )

        if features["total_lines"] < cls.MIN_LINES:

            return {

                "success": False,

                "message": f"Please provide at least {cls.MIN_LINES} lines of code."

            }

        features["language"] = cls.LANGUAGE_MAP.get(

            language,

            -1

        )

        import pandas as pd

        X = pd.DataFrame(

            [

                [

                    features[column]

                    for column in cls.FEATURE_COLUMNS

                ]

            ],

            columns=cls.FEATURE_COLUMNS

        )

        prediction = cls.model.predict(X)[0]

        probabilities = cls.model.predict_proba(X)[0]

        ai_probability = float(round(

            probabilities[1] * 100,

            2

        ) )

        human_probability = float(round(

            probabilities[0] * 100,

            2

        ) )

        confidence = float(max(

            ai_probability,

            human_probability

        ) )

        if confidence < cls.CONFIDENCE_THRESHOLD:

            result = "Uncertain"

        elif prediction == 1:

            result = "AI Generated"

        else:

            result = "Human Written"

        processing_time = round(

            time.perf_counter() - start,

            4

        )

        return {

    "success": True,

    "prediction": result,

    "confidence": confidence,

    "ai_probability": ai_probability,

    "human_probability": human_probability,

    "language": language,

    "processing_time": f"{processing_time} sec",

    "model": {

        "name": "XGBoost Classifier",

        "version": "1.0"

    }

}