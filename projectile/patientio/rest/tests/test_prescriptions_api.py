from rest_framework import status

from common.base_test import PatientBaseApiTestCase

from . import urlhelpers


class PrivatePrescriptionApiTest(PatientBaseApiTestCase):
    """Test case for Patient Prescription API"""

    def setUp(self):
        super(PrivatePrescriptionApiTest, self).setUp()

    def test_prescription_list(self):
        """Test for get prescription list"""

        response = self.client.get(urlhelpers.prescription_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_prescription_detail(self):
        # Test for retrieve prescription details

        response = self.client.get(
            urlhelpers.prescription_detail_url(self.prescription_create.data["uid"])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.prescription_create.data["uid"])
