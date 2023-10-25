import openpyxl
from django.http import FileResponse, HttpResponse
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


def export_excel(request, pk):
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="project.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Write header row
    header = ["Паспорт проекта"]
    for col_num, column_title in enumerate(header, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = column_title

    # Write data rows
    project = ProjectPlan.objects.get(id=pk)
    worksheet.title = str(project.id)

    worksheet.cell(row=1, column=1).value = 1
    worksheet.cell(row=1, column=2).value = "ID"
    worksheet.cell(row=1, column=3).value = str(project.id)
    worksheet.cell(row=2, column=1).value = 2
    worksheet.cell(row=2, column=2).value = "Наименование проекта"
    worksheet.cell(row=2, column=3).value = project.name
    worksheet.cell(row=3, column=1).value = 3
    worksheet.cell(row=3, column=2).value = "Заказчик"
    worksheet.cell(row=3, column=3).value = project.customer
    worksheet.cell(row=4, column=1).value = 4
    worksheet.cell(row=4, column=2).value = "Ответственные организации за реализацию проекта"
    worksheet.cell(row=4, column=3).value = project.responsible_subject_for_project
    worksheet.cell(row=5, column=1).value = 5
    worksheet.cell(row=5, column=2).value = "Основания для реализации проекта"
    worksheet.cell(row=5, column=3).value = project.legal_basis
    worksheet.cell(row=6, column=1).value = 6
    worksheet.cell(row=6, column=2).value = "Источники финансирования"
    worksheet.cell(row=6, column=3).value = project.source_of_financing
    worksheet.cell(row=7, column=1).value = 7
    worksheet.cell(
        row=7, column=2
    ).value = "Включен ли проект в государственную программу развития Республики Узбекистан"
    worksheet.cell(row=7, column=3).value = project.involved_in_development_country
    worksheet.cell(row=8, column=1).value = 8
    worksheet.cell(row=8, column=2).value = "Тип проекта"
    worksheet.cell(row=8, column=3).value = project.customer_status
    worksheet.cell(row=9, column=1).value = 9
    worksheet.cell(row=9, column=2).value = "Цель проекта"
    worksheet.cell(row=9, column=3).value = project.purpose
    worksheet.cell(row=10, column=1).value = 10
    worksheet.cell(row=10, column=2).value = "Задачи проекта"
    worksheet.cell(row=10, column=3).value = project.objective
    worksheet.cell(row=11, column=1).value = 11
    worksheet.cell(row=11, column=2).value = "Ориентировочная дата начала проекта"
    worksheet.cell(row=11, column=3).value = project.start_time
    worksheet.cell(row=12, column=1).value = 12
    worksheet.cell(row=12, column=2).value = "Ориентировочная дата оканчания проекта"
    worksheet.cell(row=12, column=3).value = project.finish_time
    worksheet.cell(row=13, column=1).value = 13
    worksheet.cell(row=13, column=2).value = "Ожидаемые результаты от реализации проекта"
    worksheet.cell(row=13, column=3).value = project.expecting_results
    worksheet.cell(row=14, column=1).value = 14
    worksheet.cell(row=14, column=2).value = "Создан в"
    worksheet.cell(row=14, column=3).value = str(project.created_by)
    workbook.save(response)

    return response


def export_excel_plan_graph_project(request, pk):
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="plan_graph.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Write header row
    header = ["ЭТАП", "НАИМЕНОВАНИЕ", "ДАТА НАЧАЛО", "ДАТА ОКОНЧАНИЕ", "СРОКИ В ДНЯХ", "СРОКИ В ЧАСАХ", "СТОИМОСТЬ"]
    for col_num, column_title in enumerate(header, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = column_title

    project = ProjectPlan.objects.get(id=pk)
    stage_list = project.stage_list()

    counter = 2
    for stage in stage_list:
        worksheet.cell(row=counter, column=1).value = stage.stage_number
        worksheet.cell(row=counter, column=2).value = stage.description
        worksheet.cell(row=counter, column=3).value = stage.start_time
        worksheet.cell(row=counter, column=4).value = stage.finish_time
        worksheet.cell(row=counter, column=5).value = stage.duration_per_day
        worksheet.cell(row=counter, column=6).value = stage.duration_per_hour
        worksheet.cell(row=counter, column=7).value = stage.total_price_stage_and_task
        for task in stage.task_list():
            counter += 1
            worksheet.cell(row=counter, column=1).value = ""
            worksheet.cell(row=counter, column=2).value = task.description
            worksheet.cell(row=counter, column=3).value = task.start_time
            worksheet.cell(row=counter, column=4).value = task.finish_time
            worksheet.cell(row=counter, column=5).value = task.duration_per_day
            worksheet.cell(row=counter, column=6).value = task.duration_per_hour
            worksheet.cell(row=counter, column=7).value = task.total_price
        counter += 1
    project = ProjectPlan.objects.get(id=pk)
    worksheet.title = str(project.id)

    workbook.save(response)

    return response
