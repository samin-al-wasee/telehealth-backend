from common.base_test import OrganizationBaseApiTestCase

from . import urlhelpers


class PrivateOrganizationApiTests(OrganizationBaseApiTestCase):
    """Test case for WEAPI"""

    def setUp(self):
        super(PrivateOrganizationApiTests, self).setUp()

    def test_retrieve_organization(self):
        """Test for retrieve organization detail"""

        response = self.client.get(urlhelpers.we_detail_url())

        self.assertEqual(response.data["name"], self.organization.name)

    def test_upate_organization(self):
        """Test for update organztion detail"""

        payload = {"name": "Telehealth"}

        response = self.client.patch(urlhelpers.we_detail_url(), payload)

        self.assertEqual(response.data["name"], payload["name"])
