from ai_detection.algorithms.perplexity import PerplexityCalculator

text = """
Artificial Intelligence is transforming healthcare by improving diagnostics
and automating repetitive tasks.
"""

print(
    PerplexityCalculator.calculate(text)
)