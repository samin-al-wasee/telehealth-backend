import logging

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from accountio.choices import OrganizationUserRole, OrganizationUserStatus
from accountio.models import Organization, OrganizationUser

from appointmentio.models import AppointmentTimeSlot, WeekDay, Ingredient, Medicine, SeekHelp
from appointmentio.choices import MedicineStatus

from core.models import User

from doctorio.models import Department
from appointmentio.models import Medicine, Ingredient

logger = logging.getLogger(__name__)
logger.warning("We are calling orm calls here but we do not like it")


class BaseOrmCallApi(APITestCase):
    # create user
    def get_user(self) -> User:
        logger.warning("Created USER with ORM calls")

        user = get_user_model().objects.create_user("+8801111111111", "test123pass")

        return user

    # create organization
    def create_organization(self) -> Organization:
        logger.warning("Created ORGANIZATION with ORM calls")

        organization = Organization.objects.create(
            name="CardiCheck",
            registration_no="456",
            status=OrganizationUserStatus.ACTIVE,
        )

        return organization

    # create organization user
    def create_organization_user(
        self, organzation: Organization, user: User
    ) -> OrganizationUser:
        logger.warning("Created ORGANIZATION USER with ORM calls")

        organization_user = OrganizationUser.objects.create(
            organization=organzation,
            user=user,
            role=OrganizationUserRole.OWNER,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

        return organization_user

    # create department
    def get_department(self):
        logger.warning("Created DEPARTMENT with ORM calls")

        department = Department.objects.create(name="Cardiology")
        return department

    # create ingredient
    def get_ingredient(self):
        logger.warning("Created INGREDIENT with ORM calls")

        ingredient = Ingredient.objects.create(name="Paracetamol")
        return ingredient

    # create medicine
    def get_medicine(self):
        logger.warning("Created MEDICINE with ORM calls")

        ingredient = self.get_ingredient()
        medicine = Medicine.objects.create(name="Napa", expiration_date="2023-10-10")
        medicine.ingredient.add(ingredient)
        return medicine

    # create seek help
    def get_seek_help(self):
        logger.warning("Created SEEK HELP with ORM calls")

        seek_help = SeekHelp.objects.create(name="Help me!")
        return seek_help

    def get_time_slot(self, organization):
        logger.warning("Created TIME SLOT with ORM calls")

        week_day = WeekDay.objects.create(organization=organization, day="MONDAY")

        time_slot = AppointmentTimeSlot.objects.create(organization=organization, weekday=week_day, schedule_time="08:00:00")
        return time_slot
