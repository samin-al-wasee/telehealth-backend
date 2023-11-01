from django.core.management.base import BaseCommand
from django.db import transaction

from rest_framework.exceptions import ValidationError

from accountio.choices import (
    OrganizationKind,
    OrganizationStatus,
    OrganizationUserStatus,
    OrganizationUserRole,
)
from accountio.models import Organization, OrganizationUser

from core.choices import UserType
from core.models import User

from doctorio.choices import DoctorStatus
from doctorio.models import Department, Doctor

from patientio.models import Patient


class Command(BaseCommand):
    help = "This will create required credentials for Organization, OrganizationUser, Doctor and Patient."

    def handle(self, *args, **options):
        with transaction.atomic():
            try:
                super_user = User.objects.create_superuser(
                    phone="+8801711111111",
                    password="test123pass",
                )
                super_user.social_security_number = "111-111-111"
                super_user.first_name = "Mainul"
                super_user.last_name = "Rahat"
                super_user.email = "mr@example.com"
                super_user.type = UserType.STAFF
                super_user.save()
            except:
                raise ValidationError("Superuser not created!")

            try:
                organization = Organization.objects.create(
                    name="CardiCheck",
                    phone="+8801711111111",
                    registration_no="11111",
                    kind=OrganizationKind.CLINIC,
                    status=OrganizationStatus.ACTIVE,
                )
            except:
                raise ValidationError("Organization not created!")

            # Create an organization user
            OrganizationUser.objects.create(
                organization=organization,
                user=super_user,
                is_default=True,
                status=OrganizationUserStatus.ACTIVE,
                role=OrganizationUserRole.OWNER,
            )

            # Create Department
            department = Department.objects.create(name="Cardiology")
            department.organization.set([organization])

            # Create 2 users for doctors
            user_one = User.objects.create_user(
                phone="+8801722222222",
                password="test123pass",
            )
            user_one.email = "sakil@gmail.com"
            user_one.first_name = "Shakil"
            user_one.last_name = "Ahmed"
            user_one.social_security_number = "222-222-222"
            user_one.type = UserType.DOCTOR
            user_one.save()

            user_two = User.objects.create_user(
                phone="+8801722222223",
                password="test123pass",
            )
            user_two.type = UserType.DOCTOR
            user_two.social_security_number = "222-222-333"
            user_two.first_name = "Sahir"
            user_two.last_name = "Jaman"
            user_two.email = "sj@gmail.com"
            user_two.save()

            # Create doctors
            Doctor.objects.create(
                user=user_one,
                name=user_one.get_name(),
                email=user_one.email,
                phone=user_one.phone,
                registration_no="111222333",
                department=department,
                experience=1,
                status=DoctorStatus.ACTIVE,
                organization=organization,
            )

            Doctor.objects.create(
                user=user_two,
                name=user_two.get_name(),
                email=user_two.email,
                phone=user_two.phone,
                registration_no="111222444",
                department=department,
                experience=1,
                status=DoctorStatus.ACTIVE,
                organization=organization,
            )

            # Create 2 users for patients
            user_one = User.objects.create_user(
                phone="+8801799999999",
                password="test123pass",
            )
            user_one.first_name = "Rokibul"
            user_one.last_name = "Islam"
            user_one.email = "ri@example.com"
            user_one.social_security_number = "111-999-111"
            user_one.type = UserType.PATIENT
            user_one.save()

            user_two = User.objects.create_user(
                phone="+8801799999998",
                password="test123pass",
            )
            user_two.first_name = "Osman"
            user_two.last_name = "Goni"
            user_two.email = "og@gmail.com"
            user_two.social_security_number = "111-999-112"
            user_two.type = UserType.PATIENT
            user_two.save()

            # Create patients
            Patient.objects.create(
                user=user_one,
                organization=organization,
            )
            Patient.objects.create(
                user=user_two,
                organization=organization,
            )

            self.stdout.write(self.style.SUCCESS("Credentials Created Successfully !"))
