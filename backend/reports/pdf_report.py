import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Table,

    TableStyle

)


class PDFReport:

    REPORT_DIRECTORY = "reports/generated"

    @staticmethod
    def generate(data):

        os.makedirs(

            PDFReport.REPORT_DIRECTORY,

            exist_ok=True

        )

        filename = (

            f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        )

        pdf_path = os.path.join(

            PDFReport.REPORT_DIRECTORY,

            filename

        )

        document = SimpleDocTemplate(pdf_path)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(

            Paragraph(

                "<b>Enterprise Plagiarism Detection Report</b>",

                styles["Title"]

            )

        )

        elements.append(

            Spacer(1,20)

        )

        overview = [

            [

                "Uploaded File",

                data["uploaded_file"]

            ],

            [

                "Matched Document",

                data["matched_document"]

            ],

            [

                "Overall Similarity",

                f'{data["overall_similarity"]}%'

            ],

            [

                "Risk Level",

                data["risk_level"]

            ],

            [

                "Processing Time",

                data["processing_time"]

            ]

        ]

        table = Table(overview)

        table.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

                ("BOTTOMPADDING",(0,0),(-1,-1),8)

            ])

        )

        elements.append(table)

        elements.append(

            Spacer(1,20)

        )

        elements.append(

            Paragraph(

                "<b>Algorithm Scores</b>",

                styles["Heading2"]

            )

        )

        scores = data["algorithm_scores"]

        score_table = Table([

            [

                "Algorithm",

                "Score"

            ],

            [

                "Semantic",

                f'{scores["semantic"]}%'

            ],

            [

                "TF-IDF",

                f'{scores["tfidf"]}%'

            ],

            [

                "Winnowing",

                f'{scores["winnowing"]}%'

            ]

        ])

        score_table.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BACKGROUND",(0,0),(-1,0),colors.lightblue),

                ("BOTTOMPADDING",(0,0),(-1,-1),8)

            ])

        )

        elements.append(score_table)

        elements.append(

            Spacer(1,20)

        )

        elements.append(

            Paragraph(

                "<b>Matched Sentences</b>",

                styles["Heading2"]

            )

        )

        if len(data["matched_sentences"]) == 0:

            elements.append(

                Paragraph(

                    "No matching sentences found.",

                    styles["BodyText"]

                )

            )

        else:

            for sentence in data["matched_sentences"]:

                elements.append(

                    Paragraph(

                        f"• {sentence}",

                        styles["BodyText"]

                    )

                )

        document.build(elements)

        return pdf_path