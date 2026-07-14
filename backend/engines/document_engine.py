from services.preprocessing_service import PreprocessingService

from algorithms.sentence_matcher import SentenceMatcher
from algorithms.tfidf_similarity import TFIDFSimilarity
from algorithms.semantic_similarity import SemanticSimilarity
from algorithms.winnowing import Winnowing
from algorithms.weighted_similarity import WeightedSimilarity
from algorithms.report_generator import ReportGenerator

from reports.pdf_report import PDFReport

from utils.timer import Timer


class DocumentEngine:

    def __init__(self):

        self.preprocessor = PreprocessingService()

        self.matcher = SentenceMatcher()

        self.semantic = SemanticSimilarity()

    def compare(self, text1: str, text2: str):

        timer = Timer()

        processed1 = self.preprocessor.preprocess(text1)

        processed2 = self.preprocessor.preprocess(text2)

        clean_text1 = processed1["cleaned_text"]

        clean_text2 = processed2["cleaned_text"]

        tfidf_score = TFIDFSimilarity.calculate(

            clean_text1,

            clean_text2

        )

        semantic_score = self.semantic.calculate(

            clean_text1,

            clean_text2

        )

        winnowing_score = Winnowing.similarity(

            clean_text1,

            clean_text2

        )

        final_score = WeightedSimilarity.calculate(

            tfidf_score,

            semantic_score,

            winnowing_score

        )

        matched_sentences = self.matcher.match(

            processed1["sentences"],

            processed2["sentences"]

        )

        processing_time = timer.stop()

        report = ReportGenerator.generate(

            overall_similarity=final_score,

            algorithm_scores={

                "tfidf": tfidf_score,

                "semantic": semantic_score,

                "winnowing": winnowing_score

            },

            matched_sentences=matched_sentences

        )

        report["processing_time"] = f"{processing_time:.2f} sec"

        if final_score >= 80:

            report["risk_level"] = "High"

        elif final_score >= 50:

            report["risk_level"] = "Medium"

        else:

            report["risk_level"] = "Low"

        pdf_data = {

            "uploaded_file": "Uploaded Document",

            "matched_document": "Compared Document",

            "overall_similarity": report["overall_similarity"],

            "risk_level": report["risk_level"],

            "processing_time": report["processing_time"],

            "algorithm_scores": report["algorithm_scores"],

            "matched_sentences": [

                sentence["document1_sentence"]

                for sentence in report["matched_sentences"]

            ]

        }

        pdf_path = PDFReport.generate(pdf_data)

        report["pdf_report"] = pdf_path

        return report