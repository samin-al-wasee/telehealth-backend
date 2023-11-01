import json

from rest_framework import status

from common.base_test import OrganizationBaseApiTestCase
from doctorio.rest.tests import urlhelpers as doctor_urlhelpers

from . import payloads, urlhelpers


class PrivateDoctorApiTests(OrganizationBaseApiTestCase):
    def setUp(self):
        super(PrivateDoctorApiTests, self).setUp()

    def test_create_doctor(self):
        """Test for organization creating doctor"""

        response = self.doctor_create
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["phone"],
            payloads.doctor_payload(self.department_uid)["phone"],
        )

    def test_get_doctor_list(self):
        """Test for organization getting doctor list"""
        response = self.client.get(urlhelpers.we_doctor_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_doctor(self):
        """Test for organization retrieving doctor detail"""
        response = self.client.get(urlhelpers.we_doctor_detail_url(self.doctor_uid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.doctor_create.data["uid"])

    def test_update_doctor(self):
        """Test for organization updating doctor"""

        payload = {"experience": 4}

        response = self.client.patch(
            urlhelpers.we_doctor_detail_url(self.doctor_uid), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["experience"], payload["experience"])

    def test_delete_doctor(self):
        """Test for deleting doctor"""
        response = self.client.delete(urlhelpers.we_doctor_detail_url(self.doctor_uid))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PrivateDoctorAppointmentApiTests(OrganizationBaseApiTestCase):
    def setUp(self):
        super(PrivateDoctorAppointmentApiTests, self).setUp()

    def test_get_appointment_list(self):
        """Test for organization get doctor appointment list"""

        response = self.client.get(
            urlhelpers.we_doctor_appointment_list_url(self.doctor_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_appointment(self):
        """Test for organization retrieve doctor appointment details"""

        response = self.client.get(
            urlhelpers.we_doctor_appointment_detail_url(
                self.doctor_uid, self.appointment_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], str(self.appointment_uid))


class PrivateDoctorAppointmentPrescriptionApiTests(OrganizationBaseApiTestCase):
    def setUp(self):
        super(PrivateDoctorAppointmentPrescriptionApiTests, self).setUp()
        self.medicine_create = self.base_orm.get_medicine()

        # login doctor
        self.doctor_login = self.client.post(
            urlhelpers.user_token_login_url(), payloads.doctor_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.doctor_login.data["access"]
        )

        # create prescription
        self.prescription_create = self.client.post(
            doctor_urlhelpers.doctor_appointment_prescription_list_url(
                self.appointment_uid
            ),
            data=json.dumps(
                payloads.prescription_payload(str(self.medicine_create.uid))
            ),
            content_type="application/json",
        )
        self.assertEqual(self.prescription_create.status_code, status.HTTP_201_CREATED)

        # organization login
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

    def test_get_appointment_prescription_list(self):
        """Test for organization get doctor appointment prescription list"""

        response = self.client.get(
            urlhelpers.we_doctor_appointment_prescription_list_url(
                self.doctor_uid, self.appointment_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_appointment_prescription(self):
        """Test for organization retrieve doctor appointment prescription detail"""

        response = self.client.get(
            urlhelpers.we_doctor_appointment_prescription_detail_url(
                self.doctor_uid,
                self.appointment_uid,
                self.prescription_create.data["uid"],
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["primary_diseases"],
            self.prescription_create.data["primary_diseases"],
        )
