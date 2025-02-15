import unittest

import nredarwin.webservice
from tests.soap import soap_response


class ServiceDetailsTest(unittest.TestCase):
    def setUp(self):
        resp = soap_response("GetServiceDetails", "service-details.xml")
        self.service_details = nredarwin.webservice.ServiceDetails(resp)

    def test_basic_details(self):
        self.assertEqual(self.service_details.sta, "15:41")
        self.assertEqual(self.service_details.eta, "On time")
        self.assertEqual(self.service_details.std, "15:43")
        self.assertEqual(self.service_details.etd, "On time")
        self.assertEqual(self.service_details.platform, "13")
        self.assertEqual(self.service_details.operator_name, "East Midlands Trains")
        self.assertEqual(self.service_details.operator_code, "EM")
        self.assertEqual(self.service_details.ata, None)
        self.assertEqual(self.service_details.atd, None)
        self.assertEqual(self.service_details.location_name, "Manchester Piccadilly")
        self.assertEqual(self.service_details.crs, "MAN")

    def test_messages(self):
        self.assertFalse(self.service_details.is_cancelled)
        self.assertEqual(self.service_details.disruption_reason, None)
        self.assertEqual(self.service_details.overdue_message, None)

    def test_calling_points(self):
        self.assertEqual(len(self.service_details.previous_calling_points), 5)
        self.assertEqual(len(self.service_details.subsequent_calling_points), 14)

        self.assertEqual(len(self.service_details.previous_calling_point_lists), 1)
        self.assertEqual(
            len(self.service_details.previous_calling_point_lists[0].calling_points),
            5,
        )
        self.assertEqual(len(self.service_details.subsequent_calling_point_lists), 1)
        self.assertEqual(
            len(self.service_details.subsequent_calling_point_lists[0].calling_points),
            14,
        )


class CallingPointsTest(unittest.TestCase):
    def setUp(self):
        resp = soap_response("GetServiceDetails", "service-details-splits-after.xml")
        self.service_details_splits_after = nredarwin.webservice.ServiceDetails(resp)

    def test_basic(self):
        self.assertEqual(
            len(self.service_details_splits_after.previous_calling_points), 5
        )
        self.assertEqual(
            len(self.service_details_splits_after.subsequent_calling_points), 18
        )

        calling_point_list = (
            self.service_details_splits_after.previous_calling_point_lists[0]
        )
        self.assertEqual(calling_point_list.service_type, "train")
        self.assertEqual(calling_point_list.service_change_required, False)
        self.assertEqual(calling_point_list.association_is_cancelled, False)

    def test_previous_calling_points(self):
        previous_calling_point_lists = (
            self.service_details_splits_after.previous_calling_point_lists
        )
        self.assertEqual(
            len(previous_calling_point_lists),
            1,
        )
        self.assertEqual(
            len(previous_calling_point_lists[0].calling_points),
            5,
        )

    def test_subsequent_calling_points(self):
        subsequent_calling_point_lists = (
            self.service_details_splits_after.subsequent_calling_point_lists
        )
        self.assertEqual(
            len(subsequent_calling_point_lists),
            2,
        )
        self.assertEqual(
            len(subsequent_calling_point_lists[0].calling_points),
            16,
        )
        self.assertEqual(
            len(subsequent_calling_point_lists[1].calling_points),
            2,
        )


if __name__ == "__main__":
    unittest.main()
