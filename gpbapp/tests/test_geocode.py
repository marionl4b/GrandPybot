import pytest
import requests
import requests_mock

from gpbapp import get_geocode

GMAP = get_geocode.GetGeocode()

@pytest.fixture()
def exp_params():
    """return a dictionary for request with right params"""
    params = {
        "key": "key",
        "address": "sacré coeur",
        "region": "fr",
        "language": "fr"
    }
    return params


@pytest.fixture()
def exp_parsed_results():
    """return a dictionary of expected parsed json response"""
    parsed_results = {
        "address": "35 Rue du Chevalier de la Barre, 75018 Paris, France",
        "longitude": 2.3431043,
        "latitude": 48.88670459999999,
        "search_term": "Rue du Chevalier de la Barre"
    }
    return parsed_results


class TestGMap:

    def test_request_ok(self, exp_params):
        """should return json dict with status: OK"""
        with requests_mock.Mocker(real_http=True) as m:
            m.get('mock://maps.googleapis.com/maps/api/geocode/json?',
                  headers=exp_params,
                  status_code=200,
                  json={"status": "OK"})
            r_exp = requests.get('mock://maps.googleapis.com/maps/api/geocode/json?').json()
            r = GMAP.get_geocode("sacré coeur")
            assert r_exp["status"] == r["status"]

    def test_valid_parsed_response(self, exp_parsed_results):
        """should return expected dictionary from json response"""
        r = GMAP.get_geocode("sacré coeur")
        parsed_results = GMAP.parse_results(r)
        assert exp_parsed_results == parsed_results

    def test_none_parsed_response(self):
        r = GMAP.get_geocode("unknown")
        parsed_results = GMAP.parse_results(r)
        assert parsed_results is None

    def test_special_search_term(self):
        """should return establishment address component"""
        response = GMAP.get_geocode("tour eiffel")
        result = GMAP.get_search_term(response)
        assert result == "Champ de Mars"

    def test_country_search_term(self):
        """should return country address component"""
        response = GMAP.get_geocode("Allemage")
        result = GMAP.get_search_term(response)
        assert result == "Allemagne"

    def test_locality_search_term(self):
        """should return locality address component"""
        response = GMAP.get_geocode("Strasbourg")
        result = GMAP.get_search_term(response)
        assert result == "Strasbourg"

    def test_empty_address(self, exp_params):
        """should intercept error before sending request"""
        empty = ""
        result = GMAP.get_geocode(empty)
        assert result is None

    def test_unknown_address(self, exp_params):
        """should return json dict with status: ZERO_RESULTS"""
        exp_params["address"] = "unknown"
        with requests_mock.Mocker(real_http=True) as m:
            m.get('mock://maps.googleapis.com/maps/api/geocode/json?',
                  headers=exp_params,
                  json={"status": "ZERO_RESULTS"})
            r_exp = requests.get('mock://maps.googleapis.com/maps/api/geocode/json?').json()
            r = GMAP.get_geocode("unknown")
            assert r_exp["status"] == r["status"]

    def test_wrong_key(self, exp_params):
        """should return json dict with status: REQUEST_DENIED"""
        exp_params["key"] = "wrong_key"
        GMAP.KEY = "wrong_key"
        with requests_mock.Mocker(real_http=True) as m:
            m.get('mock://maps.googleapis.com/maps/api/geocode/json?',
                  headers=exp_params,
                  json={"status": "REQUEST_DENIED"})
            r_exp = requests.get('mock://maps.googleapis.com/maps/api/geocode/json?').json()
            r = GMAP.get_geocode("sacré coeur")
            assert r_exp["status"] == r["status"]
