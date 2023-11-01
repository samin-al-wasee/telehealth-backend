from django.db import transaction
from django.core.management.base import BaseCommand, CommandParser, CommandError

import random

from uuid import uuid4

from faker import Faker

from accountio.models import Organization

from core.choices import UserType
from core.models import User

from patientio.models import Patient


class Command(BaseCommand):
    help = "Generate fake users and patients"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count",
            type=int,
            help="Number of fake user and patiend to be create",
            default=5,
        )

    def handle(self, *args, **kwargs):
        count = kwargs.get("count")
        fake = Faker()

        try:
            organization = Organization.objects.get(name="CardiCheck")
        except:
            raise CommandError("Run 'generate_credentials' management command first!")

        generate_users = []
        generate_patients = []

        for _ in range(count):
            unique_number = random.randint(1, 10000)

            phone_number = (
                self.generate_custom_bangladeshi_phone_number(fake)
                + f"{random.randint(1,9)}"
            )
            email = "test-{}@gmail.com".format(uuid4().hex)
            social_security_number = fake.random_number(10, True) + unique_number

            user = User(
                first_name=fake.first_name() + f"{unique_number}",
                last_name=fake.last_name(),
                username=phone_number,
                email=email,
                phone=phone_number,
                social_security_number=social_security_number,
                type=UserType.PATIENT,
            )

            generate_users.append(user)

        with transaction.atomic():
            User.objects.bulk_create(generate_users)

            for user in generate_users:
                patient = Patient(
                    serial_number=user.social_security_number + unique_number,
                    user=user,
                    organization=organization,
                )

                generate_patients.append(patient)

            Patient.objects.bulk_create(generate_patients)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {count} fake users and patients"
                )
            )

    def generate_custom_bangladeshi_phone_number(self, fake):
        return fake.numerify("+88011#######")
