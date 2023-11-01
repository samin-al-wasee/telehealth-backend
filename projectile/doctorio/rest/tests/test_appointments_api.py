from rest_framework import status

from common.base_test import DoctorBaseApiTestCase

from . import urlhelpers, payloads

from doctorio.rest.tests import (
    payloads as doctor_payloads,
    urlhelpers as doctor_urlhelpers,
)


class PrivateDoctorAppointmentApiTests(DoctorBaseApiTestCase):
    def setUp(self):
        super(PrivateDoctorAppointmentApiTests, self).setUp()

        self.new_prescription_create = self.client.post(
            doctor_urlhelpers.doctor_appointment_prescription_list_url(
                self.patient_appointment_uid
            ),
            doctor_payloads.prescription_payload(self.medicine_doses),
            format="json",
        )

    def test_appointment_list(self):
        """Test case for doctor getting an appointment list"""

        response = self.client.get(urlhelpers.doctor_appointment_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_appointment_detail(self):
        """Test for doctor retrieve appointment details"""

        response = self.client.get(
            urlhelpers.doctor_appointment_detail_url(self.patient_appointment_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.patient_appointment_uid)

    def test_appointment_update(self):
        """Test for doctor update appointment details"""

        response = self.client.patch(
            urlhelpers.doctor_appointment_detail_url(self.patient_appointment_uid),
            {"prescriptions": self.new_prescription_create},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["prescriptions"][0]["uid"],
            self.new_prescription_create.data["uid"],
        )

    def test_appointment_prescription_create(self):
        """Test case for doctor create an appointment's prescriptions list"""

        response = self.prescription_create

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["treatments"][0]["medicine"]["uid"], str(self.medicine.uid)
        )

    def test_doctor_appointment_prescription_list(self):
        """Test case for doctor getting an appointment's prescriptions list"""

        response = self.client.get(
            urlhelpers.doctor_appointment_prescription_list_url(
                self.patient_appointment_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_doctor_appointment_prescription_detail(self):
        """Test case for doctor getting an appointment's prescriptions details"""

        response = self.client.get(
            urlhelpers.doctor_appointment_prescription_detail_url(
                self.patient_appointment_uid, self.prescription_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["treatments"][0]["medicine"]["uid"], str(self.medicine.uid)
        )

    def test_doctor_appointment_feedback_create(self):
        """Test case for doctor can post appointment feedback"""

        response = self.client.post(
            urlhelpers.doctor_appointment_feedback_url(self.patient_appointment_uid),
            payloads.doctor_appointment_feedback_payload(),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["comment"],
            payloads.doctor_appointment_feedback_payload()["comment"],
        )

    def test_doctor_appointment_patient_medical_records(self):
        """Test case for doctor getting an appointment's patient medical records details"""

        response = self.client.get(
            urlhelpers.doctor_appointment_patient_medical_records(
                self.patient_appointment_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
