from c20_server import documentsIDs
from dotenv import load_dotenv
import os

# import requests
# import pytest
# import requests_mock
# import json


URL = "https://api.data.gov:443/regulations/v3/documents.json"
load_dotenv()
api_key = os.getenv("KEY")
dktid = "EPA-HQ-OAR-2011-0028"

api_url = "{}?api_key={}&dktid={}".format(URL, api_key, dktid)


def test_get_response(requests_mock):
    return_json = {'documents': [{'documentId': 'EPA-HQ-OAR-2011-0028-0041'}]}
    requests_mock.get(api_url,
                      json=return_json,
                      status_code=200)

    # getting list of documents IDS
    resp = documentsIDs.get_documents_ids(api_key, dktid)

    assert resp[0] == ['EPA-HQ-OAR-2011-0028-0041']


def test_bad_docketID(requests_mock):
    dktid2 = 'EPA-HQ-0000'
    api_url1 = "{}?api_key={}&dktid={}".format(URL, api_key, dktid2)
    requests_mock.get(api_url1, json=[], status_code=200)

    # getting empty data list
    resp = documentsIDs.get_documents_ids(api_key, dktid2)

    assert resp[0] == []


def test_status_code_2OO(requests_mock):
    return_json = {'documents': [{'documentId': 'EDA-MP-OAR-2017-2244-1199'}]}
    requests_mock.get(api_url, json=return_json, status_code=200)

    # getting list of documents IDS
    resp = documentsIDs.get_documents_ids(api_key, dktid)

    assert resp[1] == 200


def test_bad_apikey(requests_mock):
    return_json = {'documents': [{'documentId': 'FOP-RM-SDF-2014-3344-9988'}]}
    api_url = "{}?api_key={}s&dktid={}".format(URL, api_key, dktid)
    requests_mock.get(api_url, json=return_json, status_code=403)

    # bad url test return 403
    resp = documentsIDs.get_documents_ids(str(api_key) + 's', dktid)

    assert resp[1] == 403
