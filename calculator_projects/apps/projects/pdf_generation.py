import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from calculator_projects.apps.projects.models import ProjectPlan
from calculator_projects.apps.stages.models import StagePlan


def pdf_generation(request, pk):
    # Create a file-like buffer to receive PDF data.
    context_dict = {}
    stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False).order_by('stage_number')
    projectplan = ProjectPlan.objects.get(id=pk)
    context_dict['stage_plan_list'] = stage_plan
    context_dict['user'] = request.user
    context_dict['projectplan'] = projectplan
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


from easy_pdf.views import PDFTemplateView


class HelloPDFView(PDFTemplateView):
    template_name = 'projects/pdf/project_pdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False).order_by('stage_number')
        projectplan = ProjectPlan.objects.get(id=pk)
        context['stage_plan_list'] = stage_plan
        context['user'] = self.request.user
        context['projectplan'] = projectplan
        return context


pdf_generation_class = HelloPDFView.as_view()


def generate_pdf(request, pk):
    stage_plan = StagePlan.objects.filter(projectPlan=pk, deleted_status=False).order_by('stage_number')
    projectplan = ProjectPlan.objects.get(id=pk)

    response = FileResponse(generate_pdf_file(stage_plan, projectplan),
                            as_attachment=True,
                            filename='book_catalog.pdf')
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
