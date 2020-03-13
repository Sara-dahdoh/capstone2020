
import os
from dotenv import load_dotenv
from c20_server import documents_ids
# import requests
# import pytest
# import requests_mock
# import json


URL = "https://api.data.gov:443/regulations/v3/documents.json"
load_dotenv()
API_KEY = os.getenv("KEY")
DKT_ID = "EPA-HQ-OAR-2011-0028"
API_URL = "{}?api_key={}&dktid={}".format(URL, API_KEY, DKT_ID)


def test_get_response(requests_mock):
    return_json = {'documents': [{'documentId': 'EPA-HQ-OAR-2011-0028-0041'}]}
    requests_mock.get(API_URL, json=return_json, status_code=200)

    # getting list of documents IDS
    resp = documents_ids.get_documents_ids(API_KEY, DKT_ID)

    assert resp[0] == ['EPA-HQ-OAR-2011-0028-0041']


def test_bad_docket_id(requests_mock):
    dktid2 = 'EPA-HQ-0000'
    api_url1 = "{}?api_key={}&dktid={}".format(URL, API_KEY, dktid2)
    requests_mock.get(api_url1, json=[], status_code=200)

    # getting empty data list
    resp = documents_ids.get_documents_ids(API_KEY, dktid2)

    assert resp[0] == []


def test_status_code_two_hundred(requests_mock):
    return_json = {'documents': [{'documentId': 'EDA-MP-OAR-2017-2244-1199'}]}
    requests_mock.get(API_URL, json=return_json, status_code=200)

    # getting list of documents IDS
    resp = documents_ids.get_documents_ids(API_KEY, DKT_ID)
    assert resp[1] == 200


def test_bad_api_key(requests_mock):
    return_json = {'documents': [{'documentId': 'FOP-RM-SDF-2014-3344-9988'}]}
    api_url = "{}?api_key={}s&dktid={}".format(URL, API_KEY, DKT_ID)
    requests_mock.get(api_url, json=return_json, status_code=403)

    # bad url test return 403
    resp = documents_ids.get_documents_ids(str(API_KEY) + 's', DKT_ID)

    assert resp[1] == 403
