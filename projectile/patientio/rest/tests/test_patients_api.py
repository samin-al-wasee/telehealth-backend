from rest_framework import status

from common.base_test import PatientBaseApiTestCase
from core.rest.tests import payloads as core_payloads
from . import urlhelpers


class PrivatePatientApiTests(PatientBaseApiTestCase):
    def setUp(self):
        super(PrivatePatientApiTests, self).setUp()
        self.medicine_create = self.base_orm.get_medicine()
        self.seek_help = self.base_orm.get_seek_help()

    def test_retrieve_details(self):
        """Test case for patient retrieve details"""

        response = self.client.get(
            urlhelpers.patient_detail_url(self.patient_create.data["uid"])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["email"],
            core_payloads.user_patient_payload(self.organization)["email"],
        )

    def test_update_details(self):
        """Test case for patient update details"""

        payload = {"first_name": "Amena"}

        response = self.client.patch(
            urlhelpers.patient_detail_url(self.patient_create.data["uid"]), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], payload["first_name"])

    def test_doctor_medicine_list(self):
        """Test case for patient get doctor medicine list"""

        response = self.client.get(urlhelpers.patient_doctor_medicine_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_seek_help_list(self):
        """Test case for patient get seek help list"""

        response = self.client.get(urlhelpers.patient_seek_help_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
