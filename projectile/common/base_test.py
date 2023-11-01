from django.db import transaction

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from appointmentio.choices import AppointmentStatus
from core.rest.tests import payloads as core_payloads, urlhelpers as core_urlhelpers
from doctorio.rest.tests import (
    payloads as doctor_payloads,
    urlhelpers as doctor_urlhelpers,
)
from patientio.rest.tests import (
    payloads as patient_payloads,
    urlhelpers as patient_urlhelpers,
)
from weapi.rest.tests import payloads as we_payloads, urlhelpers as we_urlhelpers

from weapi.rest.tests import payloads as we_payloads, urlhelpers as we_urlhelpers

from .base_orm import BaseOrmCallApi


class OrganizationBaseApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_orm = BaseOrmCallApi()
        self.user = self.base_orm.get_user()

        # create organization
        self.organization = self.base_orm.create_organization()

        # connect user to organization
        self.organization_user = self.base_orm.create_organization_user(
            self.organization, self.user
        )

        # login organization user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        # creating a new patient
        self.patient_create = self.client.post(
            we_urlhelpers.we_patient_list_url(),
            core_payloads.user_patient_payload(self.organization),
        )
        
        self.assertEqual(self.patient_create.status_code, status.HTTP_201_CREATED)

        # create department
        self.create_department = self.client.post(
            we_urlhelpers.we_organization_department_list_url(),
            we_payloads.department_payload(),
        )
        self.department_uid = self.create_department.data["uid"]

        # creating a new doctor
        self.doctor_create = self.client.post(
            we_urlhelpers.we_doctor_list_url(),
            we_payloads.doctor_payload(self.department_uid),
        )

        self.assertEqual(self.doctor_create.status_code, status.HTTP_201_CREATED)

        self.patient_list = self.client.get(we_urlhelpers.we_patient_list_url())
        self.patient_uid = self.patient_list.data["results"][0]["uid"]

        self.doctor_uid = self.doctor_create.data["uid"]

        # create an appointment schedule
        self.appointment_schedule_create = self.client.post(
            we_urlhelpers.we_appointment_schedule_create_url(),
            we_payloads.appointment_schedule_payload(),
            format="json",
        )

        # get date time slot
        self.date_time_slot = self.client.get(
            we_urlhelpers.we_appointment_time_slot_list_url()
        )

        self.date = "2023-07-21"
        self.slot = self.date_time_slot.data["2023-07-21T02:00:00Z"][0]["slot"]
        self.slot_date = self.slot.date()
        self.slot_time = self.slot.time().strftime("%H:%M")

        # create an appointment
        self.appointment_create_with_doctor = self.client.post(
            we_urlhelpers.we_appointment_list_url(),
            we_payloads.appointment_with_doctor_payload(
                self.doctor_uid, self.slot_date, self.slot_time
            ),
        )

        self.appointment_uid = self.appointment_create_with_doctor.data["uid"]


class DoctorBaseApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_orm = BaseOrmCallApi()
        self.user = self.base_orm.get_user()

        # create organization
        self.organization = self.base_orm.create_organization()

        # connect user to organization
        self.organization_user = self.base_orm.create_organization_user(
            self.organization, self.user
        )

        # login organization user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        # create an appointment schedule
        self.appointment_schedule_create = self.client.post(
            we_urlhelpers.we_appointment_schedule_create_url(),
            we_payloads.appointment_schedule_payload(),
            format="json",
        )

        # get date time slot
        self.date_time_slot = self.client.get(
            we_urlhelpers.we_appointment_time_slot_list_url()
        )

        # get date and time
        self.slot = self.date_time_slot.data["2023-07-21T02:00:00Z"][0]["slot"]
        self.slot_date = self.slot.date()
        self.slot_time = self.slot.time().strftime("%H:%M")

        # creating a new patient
        self.patient_create = self.client.post(
            we_urlhelpers.we_patient_list_url(),
            core_payloads.user_patient_payload(self.organization),
        )
        self.assertEqual(self.patient_create.status_code, status.HTTP_201_CREATED)

        self.patient_uid = self.patient_create.data["uid"]

        # create department
        self.create_department = self.client.post(
            we_urlhelpers.we_organization_department_list_url(),
            we_payloads.department_payload(),
        )
        self.department_uid = self.create_department.data["uid"]

        # creating a new doctor
        self.doctor_create = self.client.post(
            we_urlhelpers.we_doctor_list_url(),
            we_payloads.doctor_payload(self.department_uid),
        )

        self.doctor_uid = self.doctor_create.data["uid"]

        self.assertEqual(self.doctor_create.status_code, status.HTTP_201_CREATED)

        # login patient
        self.patient_login = self.client.post(
            patient_urlhelpers.user_token_login_url(),
            patient_payloads.patient_login_payload(),
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.patient_login.data["access"]
        )

        # Create an appointment
        self.patient_appointment_create = self.client.post(
            patient_urlhelpers.patient_appointment_list_url(),
            patient_payloads.appointment_patient_payload(
                self.organization, self.slot_date, self.slot_time
            ),
        )

        self.assertEqual(
            self.patient_appointment_create.status_code, status.HTTP_201_CREATED
        )

        self.patient_appointment_uid = self.patient_appointment_create.data["uid"]

        # login organization user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        payload = {"doctor_uid": self.doctor_uid}

        self.patient_appointment_create = self.client.patch(
            we_urlhelpers.we_appointment_detail_url(self.patient_appointment_uid),
            payload,
        )

        # doctor's login
        self.doctor_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.doctor_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.doctor_login.data["access"]
        )

        # Get medicine
        self.medicine = self.base_orm.get_medicine()

        self.medicine_doses = [
            {
                "medicine_uid": self.medicine.uid,
                "duration": "duration_1",
                "indication": "indication_1",
                "interval": "interval_1",
            },
        ]

        # Create prescription and update appointment status to "COMPLETED"
        with transaction.atomic():
            self.prescription_create = self.client.post(
                doctor_urlhelpers.doctor_appointment_prescription_list_url(
                    self.patient_appointment_uid
                ),
                doctor_payloads.prescription_payload(self.medicine_doses),
                format="json",
            )

            payload = {"status": AppointmentStatus.COMPLETED}
            self.patient_appointment_create = self.client.patch(
                doctor_urlhelpers.doctor_appointment_detail_url(
                    self.patient_appointment_uid
                ),
                payload,
            )

        self.assertEqual(self.prescription_create.status_code, status.HTTP_201_CREATED)

        self.prescription_uid = self.prescription_create.data["uid"]


class PatientBaseApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_orm = BaseOrmCallApi()
        self.user = self.base_orm.get_user()

        # create organization
        self.organization = self.base_orm.create_organization()

        # connect user to organization
        self.organization_user = self.base_orm.create_organization_user(
            self.organization, self.user
        )

        # login organization user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        # create an appointment schedule
        self.appointment_schedule_create = self.client.post(
            we_urlhelpers.we_appointment_schedule_create_url(),
            we_payloads.appointment_schedule_payload(),
            format="json",
        )

        # get date time slot
        self.date_time_slot = self.client.get(
            we_urlhelpers.we_appointment_time_slot_list_url()
        )

        self.date = "2023-07-21"
        self.slot = self.date_time_slot.data["2023-07-21T02:00:00Z"][0]["slot"]
        self.slot_date = self.slot.date()
        self.slot_time = self.slot.time().strftime("%H:%M")

        # creating a new patient
        self.patient_create = self.client.post(
            we_urlhelpers.we_patient_list_url(),
            core_payloads.user_patient_payload(self.organization),
        )
        self.assertEqual(self.patient_create.status_code, status.HTTP_201_CREATED)

        # create department
        self.create_department = self.client.post(
            we_urlhelpers.we_organization_department_list_url(),
            we_payloads.department_payload(),
        )
        self.department_uid = self.create_department.data["uid"]

        # creating a new doctor
        self.doctor_create = self.client.post(
            we_urlhelpers.we_doctor_list_url(),
            we_payloads.doctor_payload(self.department_uid),
        )

        self.doctor_uid = self.doctor_create.data["uid"]

        self.assertEqual(self.doctor_create.status_code, status.HTTP_201_CREATED)

        # login patient
        self.patient_login = self.client.post(
            patient_urlhelpers.user_token_login_url(),
            patient_payloads.patient_login_payload(),
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.patient_login.data["access"]
        )

        # Create an appointment
        self.patient_appointment_create = self.client.post(
            patient_urlhelpers.patient_appointment_list_url(),
            patient_payloads.appointment_patient_payload(
                self.organization, self.slot_date, self.slot_time
            ),
        )

        self.assertEqual(
            self.patient_appointment_create.status_code, status.HTTP_201_CREATED
        )

        self.patient_appointment_uid = self.patient_appointment_create.data["uid"]

        # login organization user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        payload = {"doctor_uid": self.doctor_uid}

        self.patient_appointment_create = self.client.patch(
            we_urlhelpers.we_appointment_detail_url(self.patient_appointment_uid),
            payload,
        )

        # doctor's login
        self.doctor_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.doctor_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.doctor_login.data["access"]
        )

        # Get medicine
        self.medicine = self.base_orm.get_medicine()

        self.medicine_doses = [
            {
                "medicine_uid": self.medicine.uid,
                "duration": "duration_1",
                "indication": "indication_1",
                "interval": "interval_1",
            },
        ]

        # Create prescription and update appointment status to "COMPLETED"
        with transaction.atomic():
            self.prescription_create = self.client.post(
                doctor_urlhelpers.doctor_appointment_prescription_list_url(
                    self.patient_appointment_uid
                ),
                doctor_payloads.prescription_payload(self.medicine_doses),
                format="json",
            )

            payload = {"status": AppointmentStatus.COMPLETED}
            self.patient_appointment_create = self.client.patch(
                doctor_urlhelpers.doctor_appointment_detail_url(
                    self.patient_appointment_uid
                ),
                payload,
            )

        self.assertEqual(self.prescription_create.status_code, status.HTTP_201_CREATED)

        self.prescription_uid = self.prescription_create.data["uid"]

        # login patient
        self.user_login = self.client.post(
            patient_urlhelpers.user_token_login_url(),
            patient_payloads.patient_login_payload(),
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )
