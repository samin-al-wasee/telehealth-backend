from rest_framework import status

from common.base_test import OrganizationBaseApiTestCase

from patientio.rest.tests import (
    payloads as patient_payloads,
    urlhelpers as patient_urlhelpers,
)

from . import urlhelpers, payloads


class PrivateOrganizationApiTests(OrganizationBaseApiTestCase):
    """Test case for ORGANIZATION API"""

    def setUp(self):
        super(PrivateOrganizationApiTests, self).setUp()

        # login patient
        self.patient_login = self.client.post(
            patient_urlhelpers.user_token_login_url(),
            patient_payloads.patient_login_payload(),
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.patient_login.data["access"]
        )

        # create a refill
        self.patient_appointment_refill = self.client.post(
            patient_urlhelpers.patient_appointment_refill_url(self.appointment_uid),
            patient_payloads.patient_appointment_refill_payload(),
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        self.refill_list = self.client.get(urlhelpers.we_organization_refill_list_url())
        self.refill_uid = self.refill_list.data["results"][0]["uid"]

    def test_get_organization_list(self):
        """Test case for get organization list"""
        response = self.client.get(urlhelpers.we_organization_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_organization_refill_list(self):
        """Test case for get organization refill list"""
        response = self.refill_list
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_organization_refill_detail(self):
        """Test case for retrieve organization refill detail"""
        response = self.client.get(
            urlhelpers.we_organization_refill_detail_url(self.refill_uid)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            patient_payloads.patient_appointment_refill_payload()["message"],
        )

    def test_update_organization_refill_detail(self):
        """Test case for retrieve organization refill detail"""
        payload = {"status": "CANCELED"}
        response = self.client.patch(
            urlhelpers.we_organization_refill_detail_url(self.refill_uid), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["status"],
            payload["status"],
        )

    def test_get_organization_department_list(self):
        """Test case for create organization department"""
        response = self.create_department
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payloads.department_payload()["name"])

    def test_get_organization_department_list(self):
        """Test case for get organization department list"""
        response = self.client.get(urlhelpers.we_organization_department_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_organization_department_detail(self):
        """Test case for retrieve organization department detail"""
        response = self.client.get(
            urlhelpers.we_organization_department_detail_url(self.department_uid)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], payloads.department_payload()["name"])
