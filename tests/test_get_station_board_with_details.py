import unittest

import nredarwin.webservice
from nredarwin.webservice import ServiceItemWithDetails
from tests.soap import soap_response


class StationBoardWithDetailsTest(unittest.TestCase):
    def setUp(self):
        resp = soap_response("GetDepBoardWithDetails", "departure-board-with-details.xml")
        self.departures = nredarwin.webservice.StationBoard(resp, item_factory=ServiceItemWithDetails)

    def test_station_details(self):
        self.assertEqual(self.departures.crs, "ECR")
        self.assertEqual(self.departures.location_name, "East Croydon")

    def test_train_service(self):
        # test a single row
        row = self.departures.train_services[0]
        self.assertEqual(row.platform, "1")
        self.assertEqual(row.operator_name, "Southern")
        self.assertEqual(row.operator_code, "SN")
        self.assertEqual(row.sta, None)
        self.assertEqual(row.eta, None)
        self.assertEqual(row.std, "16:42")
        self.assertEqual(row.etd, "16:51")
        self.assertEqual(row.destination_text, "London Victoria")
        self.assertEqual(row.origin_text, "Littlehampton")
        self.assertFalse(row.is_circular_route)
        self.assertEqual(row.service_id, "4125791ECROYDN_")

    def test_firstDepartureCallingPoints(self):
        first_departure_calling_points = self.departures.train_services[0].subsequent_calling_point_lists[
            0].calling_points
        self.assertEqual(len(first_departure_calling_points), 2)

        self.assertEqual(first_departure_calling_points[0].location_name, "Clapham Junction")
        self.assertEqual(first_departure_calling_points[0].crs, "CLJ")
        self.assertEqual(first_departure_calling_points[0].st, "16:51")
        self.assertEqual(first_departure_calling_points[0].et, "17:00")
        self.assertEqual(first_departure_calling_points[0].length, "8")

        self.assertEqual(first_departure_calling_points[1].location_name, "London Victoria")
        self.assertEqual(first_departure_calling_points[1].crs, "VIC")
        self.assertEqual(first_departure_calling_points[1].st, "16:58")
        self.assertEqual(first_departure_calling_points[1].et, "17:07")
        self.assertEqual(first_departure_calling_points[1].length, "8")

    def test_secondDepartureCallingPoints(self):
        second_departure_calling_points = self.departures.train_services[1].subsequent_calling_point_lists[
            0].calling_points
        self.assertEqual(len(second_departure_calling_points), 14)

        self.assertEqual(second_departure_calling_points[0].location_name, "London Bridge")
        self.assertEqual(second_departure_calling_points[0].crs, "LBG")
        self.assertEqual(second_departure_calling_points[0].st, "17:00")
        self.assertEqual(second_departure_calling_points[0].et, "17:05")
        self.assertEqual(second_departure_calling_points[0].length, "12")

        self.assertEqual(second_departure_calling_points[7].location_name, "Hitchin")
        self.assertEqual(second_departure_calling_points[7].crs, "HIT")
        self.assertEqual(second_departure_calling_points[7].st, "17:50")
        self.assertEqual(second_departure_calling_points[7].et, "17:52")
        self.assertEqual(second_departure_calling_points[7].length, "12")

    def test_bus_services(self):
        """This board has no bus services"""
        self.assertEqual(self.departures.bus_services, [])

    def test_ferry_services(self):
        """This board has no ferry services"""
        self.assertEqual(self.departures.ferry_services, [])

    def test_train_service_location(self):
        # test a generic location object
        destination = self.departures.train_services[0].destinations[0]
        self.assertEqual(destination.location_name, "London Victoria")
        self.assertEqual(destination.crs, "VIC")
        self.assertEqual(destination.via, None)

    def test_nrcc_messages(self):
        self.assertEqual(
            self.departures.nrcc_messages[0],
            '\nMajor disruption to Thameslink services. Trains may be cancelled, revised or delayed by up to 20 minutes. Latest information can be found in <a href="https://www.nationalrail.co.uk/service-disruptions/london-blackfriars-20250213/">Status and Disruptions.</a>',
        )


class StationBoardArrivalDepartureWithDetailsTest(unittest.TestCase):

    def setUp(self):
        resp = soap_response("GetArrDepBoardWithDetails", "arrival-departure-board-with-details.xml")
        self.arrivals_departures = nredarwin.webservice.StationBoard(resp, item_factory=ServiceItemWithDetails)

    def test_firstDepartureCallingPoints(self):
        first_departure_calling_points = self.arrivals_departures.train_services[0].subsequent_calling_point_lists[
            0].calling_points
        self.assertEqual(len(first_departure_calling_points), 2)

        self.assertEqual(first_departure_calling_points[0].location_name, "Clapham Junction")
        self.assertEqual(first_departure_calling_points[0].crs, "CLJ")
        self.assertEqual(first_departure_calling_points[0].st, "16:51")
        self.assertEqual(first_departure_calling_points[0].et, "17:00")
        self.assertEqual(first_departure_calling_points[0].length, "8")

        self.assertEqual(first_departure_calling_points[1].location_name, "London Victoria")
        self.assertEqual(first_departure_calling_points[1].crs, "VIC")
        self.assertEqual(first_departure_calling_points[1].st, "16:58")
        self.assertEqual(first_departure_calling_points[1].et, "17:07")
        self.assertEqual(first_departure_calling_points[1].length, "8")

    def test_secondDepartureCallingPoints(self):
        second_departure_calling_points = self.arrivals_departures.train_services[1].subsequent_calling_point_lists[
            0].calling_points
        self.assertEqual(len(second_departure_calling_points), 14)

        self.assertEqual(second_departure_calling_points[0].location_name, "London Bridge")
        self.assertEqual(second_departure_calling_points[0].crs, "LBG")
        self.assertEqual(second_departure_calling_points[0].st, "17:00")
        self.assertEqual(second_departure_calling_points[0].et, "17:05")
        self.assertEqual(second_departure_calling_points[0].length, "12")

        self.assertEqual(second_departure_calling_points[7].location_name, "Hitchin")
        self.assertEqual(second_departure_calling_points[7].crs, "HIT")
        self.assertEqual(second_departure_calling_points[7].st, "17:50")
        self.assertEqual(second_departure_calling_points[7].et, "17:52")
        self.assertEqual(second_departure_calling_points[7].length, "12")


class StationBoardArrivalWithDetailsTest(unittest.TestCase):

    def setUp(self):
        resp = soap_response("GetArrBoardWithDetails", "arrival-board-with-details.xml")
        self.next_arrivals = nredarwin.webservice.StationBoard(resp, item_factory=ServiceItemWithDetails)

    def test_firstDepartureCallingPoints(self):
        first_arrival: ServiceItemWithDetails = self.next_arrivals.train_services[0]
        first_arrival_previous_calling_points = first_arrival.previous_calling_point_lists[0].calling_points
        self.assertEqual(len(first_arrival_previous_calling_points), 16)

        self.assertEqual(first_arrival_previous_calling_points[0].location_name, "Littlehampton")
        self.assertEqual(first_arrival_previous_calling_points[0].crs, "LIT")
        self.assertEqual(first_arrival_previous_calling_points[0].st, "15:12")
        self.assertEqual(first_arrival_previous_calling_points[0].et, None)
        self.assertEqual(first_arrival_previous_calling_points[0].length, "8")

        self.assertEqual(first_arrival_previous_calling_points[1].location_name, "Angmering")
        self.assertEqual(first_arrival_previous_calling_points[1].crs, "ANG")
        self.assertEqual(first_arrival_previous_calling_points[1].st, "15:21")
        self.assertEqual(first_arrival_previous_calling_points[1].et, None)
        self.assertEqual(first_arrival_previous_calling_points[1].length, "8")

        self.assertEqual(first_arrival_previous_calling_points[13].location_name, "Burgess Hill")
        self.assertEqual(first_arrival_previous_calling_points[13].crs, "BUG")
        self.assertEqual(first_arrival_previous_calling_points[13].st, "16:07")
        self.assertEqual(first_arrival_previous_calling_points[13].et, None)
        self.assertEqual(first_arrival_previous_calling_points[13].length, "8")

    def test_secondDepartureCallingPoints(self):
        second_arrival: ServiceItemWithDetails = self.next_arrivals.train_services[1]
        second_arrival_previous_calling_points = second_arrival.previous_calling_point_lists[0].calling_points
        self.assertEqual(len(second_arrival_previous_calling_points), 12)

        self.assertEqual(second_arrival_previous_calling_points[0].location_name, "Horsham")
        self.assertEqual(second_arrival_previous_calling_points[0].crs, "HRH")
        self.assertEqual(second_arrival_previous_calling_points[0].st, "15:55")
        self.assertEqual(second_arrival_previous_calling_points[0].et, None)
        self.assertEqual(second_arrival_previous_calling_points[0].length, "12")

        self.assertEqual(second_arrival_previous_calling_points[7].location_name, "Salfords")
        self.assertEqual(second_arrival_previous_calling_points[7].crs, "SAF")
        self.assertEqual(second_arrival_previous_calling_points[7].st, "16:24")
        self.assertEqual(second_arrival_previous_calling_points[7].et, None)
        self.assertEqual(second_arrival_previous_calling_points[7].length, None)
