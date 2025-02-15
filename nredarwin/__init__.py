from nredarwin.webservice import DarwinLdbSession

if __name__ == '__main__':
    darwin_client = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx")

    darwin_client.get_station_board("ECR", 10, include_departures=False, include_arrivals=False)
