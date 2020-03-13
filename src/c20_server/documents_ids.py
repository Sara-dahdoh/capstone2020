# import os
# from dotenv import load_dotenv
import requests
from c20_server import reggov_api_doc_error


def get_documents_ids(api_key, docket_id):
    api_url = "https://api.data.gov:443/regulations/v3/documents.json"
    url = "{}?api_key={}&dktid={}".format(api_url, api_key, docket_id)

    response = requests.get(url)
    if response.status_code == 403:
        raise reggov_api_doc_error.IncorrectApiKeyException
    if response.status_code == 404:
        raise reggov_api_doc_error.BadDocIDException
    if response.status_code == 400:
        raise reggov_api_doc_error.IncorrectIDPatternException
    if response.status_code == 429:
        raise reggov_api_doc_error.ExceedCallLimitException
    documents = response.json().get('documents')
    documents_ids = [document['documentId'] for document in documents]
    return documents_ids, 200
