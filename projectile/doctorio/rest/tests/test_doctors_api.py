from rest_framework import status

from common.base_test import DoctorBaseApiTestCase

from core.rest.tests import payloads as core_payloads

from . import urlhelpers, payloads


class PrivateDoctorApiTests(DoctorBaseApiTestCase):
    """Test case for DOCTOR API"""

    def setUp(self):
        super(PrivateDoctorApiTests, self).setUp()

    def test_retrieve_detail(self):
        """Test case for doctor retrieve details"""

        response = self.client.get(urlhelpers.doctor_detail_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["email"],
            payloads.doctor_payload(self.create_department)["email"],
        )

    def test_update_detail(self):
        """Test case for doctor update details"""
        payload = {"first_name": "Dr. Mosaddek", "last_name": "Mitro"}

        response = self.client.patch(urlhelpers.doctor_detail_url(), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Dr. Mosaddek Mitro")

    def test_reset_password(self):
        """Test case for doctor reset password"""

        response = self.client.put(
            urlhelpers.doctor_reset_password_url(), payloads.doctor_password_reset()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PrivateDoctorMedicineApiTests(DoctorBaseApiTestCase):
    """Test case for DOCTOR MEDICINE API"""

    def setUp(self):
        super(PrivateDoctorMedicineApiTests, self).setUp()

        self.medicine = self.base_orm.get_medicine()

    def test_medicine_list(self):
        """Test case for doctor's get medicine list"""

        response = self.client.get(urlhelpers.doctor_medicine_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["name"],
            payloads.medicine_payload()["name"],
        )

    def test_medicine_detail(self):
        """Test case for doctor's get medicine detail"""

        response = self.client.get(
            urlhelpers.doctor_medicine_detail_url(self.medicine.uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["name"],
            payloads.medicine_payload()["name"],
        )


class PrivateDoctorPatientApiTests(DoctorBaseApiTestCase):
    """Test case for Doctor Patient Api"""

    def setUp(self):
        super(PrivateDoctorPatientApiTests, self).setUp()

        # getting patient uid
        self.patient = self.client.get(urlhelpers.doctor_patient_list_url())
        self.patient_uid = self.patient.data["results"][0]["uid"]

    def test_patient_list(self):
        """Test case for doctor's get patient list"""

        response = self.client.get(urlhelpers.doctor_patient_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["patient"]["email"],
            core_payloads.user_patient_payload(self.organization)["email"],
        )

    def test_patient_detail(self):
        """Test case for doctor's get patient details"""

        response = self.client.get(
            urlhelpers.doctor_patient_detail_url(self.patient_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["patient"]["email"],
            core_payloads.user_patient_payload(self.organization)["email"],
        )
