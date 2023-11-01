from rest_framework import status

from common.base_test import PatientBaseApiTestCase

from . import urlhelpers


class PrivateNotificationsApiTest(PatientBaseApiTestCase):
    """Test case for Patient Notification API"""

    def setUp(self):
        super(PrivateNotificationsApiTest, self).setUp()

        self.notification_response = self.client.get(urlhelpers.notification_list_url())
        self.notification_uid = self.notification_response.data["results"][0]["uid"]

    def test_notification_list(self):
        """Test for get notification list"""

        response = self.client.get(urlhelpers.notification_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 4)

    def test_notification_detail(self):
        """Test for retrieve notification details"""

        response = self.client.get(
            urlhelpers.notification_detail_url(self.notification_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.notification_uid)
