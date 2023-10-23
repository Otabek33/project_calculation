from django.http import FileResponse
from reportlab.pdfgen import canvas

from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.stages.models import StagePlan


def generate_pdf(request, pk):
    stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False).order_by("stage_number")
    projectplan = ProjectPlan.objects.get(id=pk)

    response = FileResponse(
        generate_pdf_file(stage_plan, projectplan), as_attachment=True, filename="book_catalog.pdf"
    )
    return response


def generate_pdf_file(stage_list, project):
    from io import BytesIO

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Create a PDF document

    p.drawString(100, 750, "Book Catalog")

    y = 700
    for stage in stage_list:
        p.drawString(100, y, f"Title: {stage.description}")
        p.drawString(100, y - 20, f"Author: {stage.start_time}")
        p.drawString(100, y - 40, f"Year: {stage.finish_time}")
        y -= 60

    p.showPage()
    p.save()

    buffer.seek(0)

    return buffer
