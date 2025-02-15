import unittest

import nredarwin.webservice
from nredarwin.webservice import ServiceItem
from tests.soap import soap_response


class StationBoardDepartureTest(unittest.TestCase):
    def setUp(self):
        resp = soap_response("GetDepartureBoard", "departure-board.xml")
        self.departures = nredarwin.webservice.StationBoard(resp)

    def test_station_details(self):
        self.assertEqual(self.departures.crs, "MAN")
        self.assertEqual(self.departures.location_name, "Manchester Piccadilly")

    def test_train_service(self):
        # test a single row
        row = self.departures.train_services[0]
        self.assertEqual(row.platform, "1")
        self.assertEqual(row.operator_name, "First TransPennine Express")
        self.assertEqual(row.operator_code, "TP")
        self.assertEqual(row.sta, None)
        self.assertEqual(row.eta, None)
        self.assertEqual(row.std, "11:57")
        self.assertEqual(row.etd, "On time")
        self.assertEqual(row.destination_text, "Middlesbrough")
        self.assertEqual(row.origin_text, "Manchester Airport")
        self.assertFalse(row.is_circular_route)
        self.assertEqual(row.service_id, "u0bRc9iGz6QPJPk0ipljgg==")

    def test_bus_services(self):
        """This board has no bus services"""
        self.assertEqual(self.departures.bus_services, [])

    def test_ferry_services(self):
        """This board has no ferry services"""
        self.assertEqual(self.departures.ferry_services, [])

    def test_train_service_location(self):
        # test a generic location object
        destination = self.departures.train_services[0].destinations[0]
        self.assertEqual(destination.location_name, "Middlesbrough")
        self.assertEqual(destination.crs, "MBR")
        self.assertEqual(destination.via, None)

    def test_nrcc_messages(self):
        self.assertEqual(
            self.departures.nrcc_messages[0],
            'Trains through Wembley Central&nbsp;are being delayed by up to\
&nbsp;40 minutes. More details can be found in <A href="    \
http://nationalrail.co.uk/service_disruptions/88961.aspx">Latest Travel News.\
</A>',
        )


class StationBoardArrivalDepartureTest(unittest.TestCase):

    def setUp(self):
        resp = soap_response("GetArrivalDepartureBoard", "arrival-departure-board.xml")
        self.arrivals_departures = nredarwin.webservice.StationBoard(resp)

    def test_basic(self):
        self.assertEqual(self.arrivals_departures.crs, "ECR")
        self.assertEqual(self.arrivals_departures.location_name, "East Croydon")

        self.assertEqual(len(self.arrivals_departures.train_services), 10)

    def test_firstDeparture(self):
        first_departure: ServiceItem = self.arrivals_departures.train_services[0]
        self.assertEqual(first_departure.sta, "16:41")
        self.assertEqual(first_departure.eta, "16:49")
        self.assertEqual(first_departure.std, "16:42")
        self.assertEqual(first_departure.etd, "16:50")
        self.assertEqual(first_departure.platform, "1")
        self.assertEqual(first_departure.operator_name, "Southern")
        self.assertEqual(first_departure.operator_code, "SN")
        self.assertEqual(first_departure.length, "8")
        self.assertEqual(first_departure.service_id, "4125791ECROYDN_")
        self.assertEqual(first_departure.origin_text, "Littlehampton")
        self.assertEqual(first_departure.origins[0].location_name, "Littlehampton")
        self.assertEqual(first_departure.origins[0].crs, "LIT")
        self.assertEqual(first_departure.destination_text, "London Victoria")
        self.assertEqual(first_departure.destinations[0].location_name, "London Victoria")
        self.assertEqual(first_departure.destinations[0].crs, "VIC")

    def test_secondDeparture(self):
        second_departure: ServiceItem = self.arrivals_departures.train_services[1]
        self.assertEqual(second_departure.sta, "16:45")
        self.assertEqual(second_departure.eta, "16:50")
        self.assertEqual(second_departure.std, "16:45")
        self.assertEqual(second_departure.etd, "16:51")
        self.assertEqual(second_departure.platform, "2")
        self.assertEqual(second_departure.operator_name, "Thameslink")
        self.assertEqual(second_departure.operator_code, "TL")
        self.assertEqual(second_departure.length, "12")
        self.assertEqual(second_departure.service_id, "4121937ECROYDN_")
        self.assertEqual(second_departure.origin_text, "Three Bridges")
        self.assertEqual(second_departure.origins[0].location_name, "Three Bridges")
        self.assertEqual(second_departure.origins[0].crs, "TBD")
        self.assertEqual(second_departure.destination_text, "Peterborough")
        self.assertEqual(second_departure.destinations[0].location_name, "Peterborough")
        self.assertEqual(second_departure.destinations[0].crs, "PBO")


class StationBoardArrivalTest(unittest.TestCase):

    def setUp(self):
        resp = soap_response("GetArrivalDepartureBoard", "arrival-board.xml")
        self.arrivals = nredarwin.webservice.StationBoard(resp)

    def test_basic(self):
        self.assertEqual(self.arrivals.crs, "ECR")
        self.assertEqual(self.arrivals.location_name, "East Croydon")

        self.assertEqual(len(self.arrivals.train_services), 10)

    def test_firstDeparture(self):
        first_departure: ServiceItem = self.arrivals.train_services[0]
        self.assertEqual(first_departure.sta, "16:41")
        self.assertEqual(first_departure.eta, "16:50")
        self.assertEqual(first_departure.std, None)
        self.assertEqual(first_departure.etd, None)
        self.assertEqual(first_departure.platform, "1")
        self.assertEqual(first_departure.operator_name, "Southern")
        self.assertEqual(first_departure.operator_code, "SN")
        self.assertEqual(first_departure.length, "8")
        self.assertEqual(first_departure.service_id, "4125791ECROYDN_")
        self.assertEqual(first_departure.origin_text, "Littlehampton")
        self.assertEqual(first_departure.origins[0].location_name, "Littlehampton")
        self.assertEqual(first_departure.origins[0].crs, "LIT")
        self.assertEqual(first_departure.destination_text, "London Victoria")
        self.assertEqual(first_departure.destinations[0].location_name, "London Victoria")
        self.assertEqual(first_departure.destinations[0].crs, "VIC")

    def test_secondDeparture(self):
        second_departure: ServiceItem = self.arrivals.train_services[1]
        self.assertEqual(second_departure.sta, "16:45")
        self.assertEqual(second_departure.eta, "16:47")
        self.assertEqual(second_departure.std, None)
        self.assertEqual(second_departure.etd, None)
        self.assertEqual(second_departure.platform, "6")
        self.assertEqual(second_departure.operator_name, "Thameslink")
        self.assertEqual(second_departure.operator_code, "TL")
        self.assertEqual(second_departure.length, "12")
        self.assertEqual(second_departure.service_id, "4121897ECROYDN_")
        self.assertEqual(second_departure.origin_text, "Peterborough")
        self.assertEqual(second_departure.origins[0].location_name, "Peterborough")
        self.assertEqual(second_departure.origins[0].crs, "PBO")
        self.assertEqual(second_departure.destination_text, "Horsham")
        self.assertEqual(second_departure.destinations[0].location_name, "Horsham")
        self.assertEqual(second_departure.destinations[0].crs, "HRH")
