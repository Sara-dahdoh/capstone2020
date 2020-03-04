import os
import requests
from dotenv import load_dotenv

def get_documents_ids(api_url, api_key, docket_id):
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



def main():
    load_dotenv()
    docket_id = 'EPA-HQ-OAR-2011-0028'
    #docket_id = 'ED-2018-OCR-0064'

    api_key = os.getenv("KEY")
    url = 'https://api.data.gov:443/regulations/v3/documents.json'

    result = get_documents_ids(url,api_key, docket_id)
    print(result)

if __name__ == "__main__":
     main()
