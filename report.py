from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_health_report(
    pet_name,
    symptom,
    result
):

    filename = f"{pet_name}_health_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Pet Healthcare AI Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Pet: {pet_name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Symptom: {symptom}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            result.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filename