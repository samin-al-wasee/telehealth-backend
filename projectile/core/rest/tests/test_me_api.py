from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common.base_orm import BaseOrmCallApi

from weapi.rest.tests import urlhelpers as we_urlhelpers, payloads as we_payloads

from . import payloads, urlhelpers


class PrivateMeApiTest(APITestCase):
    # Test case for ME API

    def setUp(self):
        self.client = APIClient()
        self.base_orm = BaseOrmCallApi()
        self.organization = self.base_orm.create_organization()
        self.user_register = self.client.post(urlhelpers.user_patient_url(), payloads.user_patient_payload(self.organization))

        # login user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), payloads.user_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

    def test_retrieve_me(self):
        # Test for retrieve user details

        response = self.client.get(urlhelpers.me_detail_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"],  payloads.user_patient_payload(self.organization)["first_name"])

    def test_update_me(self):
        # Test for update user

        new_payload = {"blood_group": "A+"}
        response = self.client.patch(urlhelpers.me_detail_url(), new_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["blood_group"], new_payload["blood_group"])
