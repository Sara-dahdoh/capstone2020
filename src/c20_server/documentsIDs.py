import os
import requests
from dotenv import load_dotenv


def get_documents_ids(api_key, docket_id):

    api_url = "https://api.data.gov:443/regulations/v3/documents.json"
    url = "{}?api_key={}&dktid={}".format(api_url,api_key,docket_id)

    response = requests.get(url)
    try:
        if response.status_code == 200:
            documents = response.json().get('documents')

            documentsIds = [document['documentId'] for document in documents]

            return documentsIds, 200

        else:
            return [], response.status_code
    except Exception:
        return [], response.status_code
