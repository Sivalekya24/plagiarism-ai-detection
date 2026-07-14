from ai_detection.analyzers.structure import StructureAnalyzer
from ai_detection.analyzers.comment import CommentAnalyzer
from ai_detection.analyzers.identifier import IdentifierAnalyzer
from ai_detection.analyzers.token import TokenAnalyzer
from ai_detection.analyzers.complexity import ComplexityAnalyzer
from ai_detection.analyzers.entropy import EntropyAnalyzer


class CodeFeatures:

    @staticmethod
    def extract(code: str):

        structure = StructureAnalyzer.analyze(code)

        comments = CommentAnalyzer.analyze(code)

        identifiers = IdentifierAnalyzer.analyze(code)

        tokens = TokenAnalyzer.analyze(code)

        complexity = ComplexityAnalyzer.analyze(code)

        entropy = EntropyAnalyzer.analyze(code)

        features = {}

        features.update(structure)

        features.update(comments)

        features.update(identifiers)

        features.update(tokens)

        features.update(complexity)

        features.update(entropy)

        return features