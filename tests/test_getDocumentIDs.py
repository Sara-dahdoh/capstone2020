from c20_server import documentsIDs
from dotenv import load_dotenv
import os
import requests
import pytest
import requests_mock
import unittest
from mock import patch
import json


URL = "https://api.data.gov:443/regulations/v3/documents.json"
load_dotenv()
api_key = os.getenv("KEY")
dktid = "EPA-HQ-OAR-2011-0028"

api_url = "{}?api_key={}&dktid={}".format(URL,api_key,dktid)


class Tests(unittest.TestCase):

    @requests_mock.mock()
    def test_get_response(self, m):

        m.get(api_url, json = {'documents': [{'documentId': 'EPA-HQ-OAR-2011-0028-0041' }]}, status_code=200)

        # getting list of documents IDS
        resp = documentsIDs.get_documents_ids(URL, api_key, dktid)

        assert resp[0] == ['EPA-HQ-OAR-2011-0028-0041']

    @requests_mock.mock()
    def test_bad_docketID(self, m):
        dktid2 = 'EPA-HQ-0000'
        api_url1 = "{}?api_key={}&dktid={}".format(URL,api_key,dktid2)
        m.get(api_url1, json = [], status_code=200)

        # getting empty data list
        resp = documentsIDs.get_documents_ids(URL, api_key, dktid2)

        assert resp[0] == []

    @requests_mock.mock()
    def test_status_code_2OO(self, m):

        m.get(api_url, json = {'documents': [{'documentId': 'EDA-MP-OAR-2017-2244-1199' }]}, status_code=200)

        # getting list of documents IDS
        resp = documentsIDs.get_documents_ids(URL, api_key, dktid)

        assert resp[1] == 200

    @requests_mock.mock()
    def test_bad_url(self, m):

        api_url = "{}s?api_key={}&dktid={}".format(URL,api_key,dktid)
        m.get(api_url, json = {'documents': [{'documentId': 'FOP-RM-SDF-2014-3344-9988' }]}, status_code=404)

        # bad url test return 404
        resp = documentsIDs.get_documents_ids(URL+"s", api_key, dktid)

        assert resp[1] == 404
