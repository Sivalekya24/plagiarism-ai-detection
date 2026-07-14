import statistics


class StructureAnalyzer:

    @staticmethod
    def analyze(code: str):

        lines = code.splitlines()

        total_lines = len(lines)

        if total_lines == 0:
            return {
                "total_lines": 0,
                "blank_lines": 0,
                "blank_line_ratio": 0,
                "average_line_length": 0,
                "max_line_length": 0,
                "min_line_length": 0,
                "line_length_variance": 0,
                "empty_line_groups": 0
            }

        blank_lines = 0
        empty_groups = 0
        previous_blank = False

        line_lengths = []

        for line in lines:

            length = len(line)
            line_lengths.append(length)

            if line.strip() == "":
                blank_lines += 1

                if not previous_blank:
                    empty_groups += 1

                previous_blank = True

            else:
                previous_blank = False

        average_line_length = statistics.mean(line_lengths)

        max_line_length = max(line_lengths)

        min_line_length = min(line_lengths)

        variance = statistics.pvariance(line_lengths)

        blank_ratio = blank_lines / total_lines

        return {

            "total_lines": total_lines,

            "blank_lines": blank_lines,

            "blank_line_ratio": round(blank_ratio, 4),

            "average_line_length": round(
                average_line_length,
                2
            ),

            "max_line_length": max_line_length,

            "min_line_length": min_line_length,

            "line_length_variance": round(
                variance,
                2
            ),

            "empty_line_groups": empty_groups

        }