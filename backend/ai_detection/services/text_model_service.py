import os
import time
import joblib

from ai_detection.algorithms.text_features import TextFeatures
from ai_detection.algorithms.text_feature_vector import TextFeatureVector


class TextModelService:
    
    MIN_WORDS = 50
    CONFIDENCE_THRESHOLD = 70.0

    MODEL_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "models",
        "text_model.pkl"
    )

    model = None

    @classmethod
    def load_model(cls):
        

        if cls.model is None:

            if not os.path.exists(cls.MODEL_PATH):
                raise FileNotFoundError(
                    f"Model not found at: {cls.MODEL_PATH}"
                )

            cls.model = joblib.load(cls.MODEL_PATH)

    @classmethod
    def predict(cls, text: str):

        cls.load_model()

        start_time = time.perf_counter()

        
        features = TextFeatures.extract(text)

        
        if features["total_words"] < cls.MIN_WORDS:

            return {

                "success": False,

                "prediction": None,

                "message": f"Please provide at least {cls.MIN_WORDS} words for reliable AI detection.",

                "current_words": features["total_words"],

                "minimum_words": cls.MIN_WORDS

            }

        
        feature_vector = TextFeatureVector.build(features)

        
        prediction = cls.model.predict(feature_vector)[0]

        probabilities = cls.model.predict_proba(feature_vector)[0]

        ai_probability = float(
            round(probabilities[1] * 100, 2)
        )

        human_probability = float(
            round(probabilities[0] * 100, 2)
        )

        confidence = max(
            ai_probability,
            human_probability
        )

       
        if confidence < cls.CONFIDENCE_THRESHOLD:

            final_prediction = "Uncertain"

        elif prediction == 1:

            final_prediction = "AI Generated"

        else:

            final_prediction = "Human Written"

        processing_time = round(
            time.perf_counter() - start_time,
            4
        )

        
        return {

    "success": True,

    "prediction": final_prediction,

    "confidence": confidence,

    "ai_probability": ai_probability,

    "human_probability": human_probability,

    "processing_time": f"{processing_time} sec",

    "minimum_words_required": cls.MIN_WORDS,

    "model": {

        "name": "XGBoost Classifier",

        "version": "1.0"

    }

}