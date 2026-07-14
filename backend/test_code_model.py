import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(CURRENT_DIR)

from ai_detection.services.code_model_service import CodeModelService


code = """
def factorial(n):

    if n <= 1:
        return 1

    result = 1

    for i in range(2, n + 1):
        result *= i

    return result


print(factorial(5))
"""

response = CodeModelService.predict(

    code=code,

    language="Python"

)

print()

print(response)