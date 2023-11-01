from rest_framework import status

from common.base_test import PatientBaseApiTestCase

from . import payloads, urlhelpers


class PatientAppointmentApiTests(PatientBaseApiTestCase):
    def setUp(self):
        super(PatientAppointmentApiTests, self).setUp()

    def test_patient_appointment_create(self):
        """Test case for patient create an appointment"""

        response = self.patient_appointment_create

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], str(self.patient_appointment_uid))

    def test_patient_appointment_list(self):
        """Test case for patient get appointments list"""

        response = self.client.get(urlhelpers.patient_appointment_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_patient_appointment_detail(self):
        """Test case for patient get appointment details"""

        response = self.client.get(
            urlhelpers.patient_appointment_detail_url(self.patient_appointment_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], str(self.patient_appointment_uid))

    def test_patient_appointment_complete_list(self):
        """Test case for patient get appointment complete list"""
        time = "10:30"

        self.patient_appointment_complete_update = self.client.put(
            urlhelpers.patient_appointment_detail_url(self.patient_appointment_uid),
            payloads.appointment_patient_status_complete_payload(
                self.organization, self.slot_date, time
            ),
        )

        response = self.client.get(urlhelpers.patient_completed_appointment_list_url())

        patient_appointment_completed_payload = (
            payloads.appointment_patient_status_complete_payload(
                self.organization, self.slot_date, self.slot_time
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["status"],
            patient_appointment_completed_payload["status"],
        )

    def test_patient_appointment_time_slot_list(self):
        """Test case for patient get appointment time slot list"""
        payload = {"date": "2023-07-21"}

        response = self.client.get(
            urlhelpers.patient_appointment_time_slot_list_url(),
            {"date": self.slot_date},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["2023-07-21T09:00:00Z"][0]["date"], payload["date"]
        )

    def test_patient_appointment_prescription_list_url(self):
        """Test case for patient get appointment prescription list"""

        response = self.client.get(
            urlhelpers.patient_appointment_prescription_list_url(
                self.patient_appointment_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.prescription_uid, response.data["results"][0]["uid"])

    def test_patient_appointment_prescription_detail_url(self):
        """Test case for patient get appointment prescription detail"""

        response = self.client.get(
            urlhelpers.patient_appointment_prescription_detail_url(
                self.patient_appointment_uid, self.prescription_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            str(self.medicine_doses[0]["medicine_uid"]),
            response.data["treatments"][0]["medicine"]["uid"],
        )

    def test_patient_appointment_feedback_create(self):
        """Test case for patient can post appointment feedback"""
        response = self.client.post(
            urlhelpers.patient_appointment_feedback_url(self.patient_appointment_uid),
            payloads.patient_appointment_feedback_payload(),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["comment"],
            payloads.patient_appointment_feedback_payload()["comment"],
        )
