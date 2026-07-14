from ai_detection.services.text_model_service import TextModelService
from ai_detection.services.code_model_service import CodeModelService


class AIEngine:

    SUPPORTED_LANGUAGES = [

        "Python",
        "Java",
        "JavaScript",
        "C",
        "C++",
        "C#",
        "Go",
        "PHP",
        "Rust"

    ]

    @staticmethod
    def detect_text(text: str):

        if text is None or not text.strip():

            return {

                "success": False,

                "message": "Input text cannot be empty."

            }

        return TextModelService.predict(text)

    @staticmethod
    def detect_code(code: str, language: str):

        if code is None or not code.strip():

            return {

                "success": False,

                "message": "Input code cannot be empty."

            }

        if language is None or not language.strip():

            return {

                "success": False,

                "message": "Programming language is required."

            }

        if language not in AIEngine.SUPPORTED_LANGUAGES:

            return {

                "success": False,

                "message": f"Unsupported language: {language}"

            }

        return CodeModelService.predict(

            code,

            language

        )

    @staticmethod
    def health():

        return {

            "success": True,

            "service": "AI Detection Engine",

            "status": "Running",

            "supported_modules": [

                "Text AI Detection",

                "Code AI Detection"

            ],

            "supported_languages": AIEngine.SUPPORTED_LANGUAGES

        }