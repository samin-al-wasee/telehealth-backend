from rest_framework import status

from appointmentio.choices import AppointmentType

from common.base_test import OrganizationBaseApiTestCase

from . import urlhelpers


class PrivateOrganizationAppointmentApiTests(OrganizationBaseApiTestCase):
    def setUp(self):
        super(PrivateOrganizationAppointmentApiTests, self).setUp()
        self.date_time_slot = self.base_orm.get_time_slot(self.organization)

    def test_create_appointment(self):
        """Test for create appointment by organization"""
        response = self.appointment_create_with_doctor
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_appointment(self):
        """Test for get appointment list by organization"""
        response = self.client.get(urlhelpers.we_appointment_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_appointment(self):
        """Test for retrieve appointment detail by organization"""
        response = self.client.get(
            urlhelpers.we_appointment_detail_url(self.appointment_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["uid"], self.appointment_uid)

    def test_update_appointment(self):
        """Test for update appointment detail by organization"""

        payload = {"appointment_type": AppointmentType.FOLLOWUP}

        response = self.client.patch(
            urlhelpers.we_appointment_detail_url(self.appointment_uid),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["appointment_type"], payload["appointment_type"])

    def test_delete_appointment(self):
        """Test for delete appointment by organization"""

        response = self.client.delete(
            urlhelpers.we_appointment_detail_url(self.appointment_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_appointment_schedule(self):
        """Test for appointment schedule create by organization"""

        response = self.appointment_schedule_create

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_appointment_time_slot_list(self):
        """Test for get appointment time-slot list by organization"""

        payload = {"date": "2023-07-21"}

        response = self.client.get(urlhelpers.we_appointment_time_slot_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["2023-07-21T09:00:00Z"][0]["date"], payload["date"]
        )
