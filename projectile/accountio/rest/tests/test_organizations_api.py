from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from common.base_orm import BaseOrmCallApi

from . import urlhelpers


class PublicOrganizationsTest(APITestCase):
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

    def test_organization_list(self):
        response = self.client.get(urlhelpers.public_organization_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.organization.name)
