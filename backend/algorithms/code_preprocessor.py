import ast
import io
import keyword
import tokenize


class IdentifierNormalizer(ast.NodeTransformer):

    def __init__(self):

        self.variables = {}
        self.functions = {}
        self.classes = {}

        self.variable_count = 1
        self.function_count = 1
        self.class_count = 1

    def visit_FunctionDef(self, node):

        if node.name not in self.functions:
            self.functions[node.name] = f"FUNC{self.function_count}"
            self.function_count += 1

        node.name = self.functions[node.name]

        self.generic_visit(node)

        return node

    def visit_ClassDef(self, node):

        if node.name not in self.classes:
            self.classes[node.name] = f"CLASS{self.class_count}"
            self.class_count += 1

        node.name = self.classes[node.name]

        self.generic_visit(node)

        return node

    def visit_arg(self, node):

        if node.arg not in self.variables:
            self.variables[node.arg] = f"VAR{self.variable_count}"
            self.variable_count += 1

        node.arg = self.variables[node.arg]

        return node

    def visit_Name(self, node):

        if keyword.iskeyword(node.id):
            return node

        if node.id not in self.variables:
            self.variables[node.id] = f"VAR{self.variable_count}"
            self.variable_count += 1

        node.id = self.variables[node.id]

        return node


class CodePreprocessor:

    @staticmethod
    def remove_comments(code):

        try:

            result = []

            tokens = tokenize.generate_tokens(
                io.StringIO(code).readline
            )

            for token in tokens:

                if token.type == tokenize.COMMENT:
                    continue

                result.append(token)

            return tokenize.untokenize(result)

        except Exception:

            return code

    @staticmethod
    def normalize_python(code):

        try:

            tree = ast.parse(code)

            tree = IdentifierNormalizer().visit(tree)

            ast.fix_missing_locations(tree)

            return ast.unparse(tree)

        except Exception:

            return code

    @staticmethod
    def normalize_whitespace(code):

        return " ".join(code.split())

    @staticmethod
    def preprocess(code):

        code = CodePreprocessor.remove_comments(code)

        code = CodePreprocessor.normalize_python(code)

        code = CodePreprocessor.normalize_whitespace(code)

        return code