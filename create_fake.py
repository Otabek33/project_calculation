def fake_date():
    from calculator_projects.apps.users.models import User, UserRoleTypes, JobTitle, Department
    import string
    faker = Faker()
    # for i in range(20):
    #     job_title = JobTitle.objects.create(
    #         name=faker.job(),
    #         code=faker.pyint(),
    #
    #     )
    #     print(f"Created job title. Name: {job_title.name}  Code: {job_title.code}")
    # job_title_list = JobTitle.objects.count()
    # print(f"There are {job_title_list} job titles in the database")

    # for i in range(10):
    #     department = Department.objects.create(
    #         name=faker.catch_phrase(),
    #         code=faker.pyint(),
    #
    #     )
    #     print(f"Created department. Name: {department.name}  Code: {department.code}")
    # department_list = Department.objects.count()
    # print(f"There are {department_list} departments in the database")

    # for i in range(30):
    #     username = string.ascii_lowercase
    #     user = User.objects.create(
    #         first_name=faker.first_name(),
    #         last_name=faker.last_name(),
    #         email=faker.ascii_company_email(),
    #         user_role=UserRoleTypes.PUBLIC_USER,
    #         job_title=random.choice(JobTitle.objects.all()),
    #         deportment=random.choice(Department.objects.all()),
    #         username=faker.first_name()+str(random.randrange(1, 100)),
    #         password=faker.vin() + "!a",
    #         is_active=True,
    #     )
    #     print(f"Created job title. Name: {user.first_name}  Username: {user.username} Password: {user.password} ")
    #
    # user_count = User.objects.count()
    #
    # print(f"There are {user_count} users in the database")


# if __name__ == "__main__":
#     import os
#
#     from django.core.wsgi import get_wsgi_application
#
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
#     application = get_wsgi_application()
#
#     import random
#     from faker import Faker
#
#     fake_date()
