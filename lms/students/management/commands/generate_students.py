from django.core.management.base import BaseCommand
from faker import Faker

from students.models import Student


class Command(BaseCommand):
    help = "Generate students"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help=u"Number of students to create")

    def handle(self, *args, **options):
        count = options["count"]
        faker = Faker()
        for i in range(count):
            Student.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                birthdate=faker.date_time_between(start_date="-30y", end_date="-18y"),
            )

    # def generate_instances(cls, count):
    #     faker = Faker()
    #     for _ in range(count):
    #         st = cls(
    #             first_name=faker.first_name(),
    #             last_name=faker.last_name(),
    #             email=faker.email(),
    #             birthdate=faker.date_time_between(start_date="-30y", end_date="-18y"),
    #         )
    #         st.save()
