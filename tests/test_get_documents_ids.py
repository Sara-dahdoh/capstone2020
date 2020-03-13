
import os
import pytest
import requests_mock
from dotenv import load_dotenv
from c20_server import documents_ids, reggov_api_doc_error
# import requests
# import pytest
# import requests_mock
# import json


URL = "https://api.data.gov:443/regulations/v3/documents.json"
load_dotenv()
API_KEY = os.getenv("KEY")
DKT_ID = "EPA-HQ-OAR-2011-0028"
API_URL = "{}?api_key={}&dktid={}".format(URL, API_KEY, DKT_ID)


def test_get_response():
    return_json = {'documents': [{'documentId': 'EPA-HQ-OAR-2011-0028-0041'}]}
    with requests_mock.Mocker() as mock:
        mock.get(API_URL, json=return_json, status_code=200)

        # getting list of documents IDS
        resp = documents_ids.get_documents_ids(API_KEY, DKT_ID)
        assert resp[0] == ['EPA-HQ-OAR-2011-0028-0041']


def test_bad_docket_id():
    dktid2 = 'EPA-HQ-0000'
    api_url1 = "{}?api_key={}&dktid={}".format(URL, API_KEY, dktid2)
    # getting empty data list
    with requests_mock.Mocker() as mock:
        mock.get(api_url1, json=[], status_code=404)
        with pytest.raises(reggov_api_doc_error.BadDocIDException):
            documents_ids.get_documents_ids(API_KEY, dktid2)


def test_status_code_two_hundred():
    return_json = {'documents': [{'documentId': 'EDA-MP-OAR-2017-2244-1199'}]}
    with requests_mock.Mocker() as mock:
        mock.get(API_URL, json=return_json, status_code=200)
    # getting list of documents IDS
        resp = documents_ids.get_documents_ids(API_KEY, DKT_ID)
        assert resp[1] == 200


def test_bad_api_key():
    return_json = {'documents': [{'documentId': 'FOP-RM-SDF-2014-3344-9988'}]}
    api_url = "{}?api_key={}s&dktid={}".format(URL, API_KEY, DKT_ID)
    with requests_mock.Mocker() as mock:
        mock.get(api_url, json=return_json, status_code=403)
        with pytest.raises(reggov_api_doc_error.IncorrectApiKeyException):
            documents_ids.get_documents_ids(str(API_KEY) + "s", DKT_ID)
