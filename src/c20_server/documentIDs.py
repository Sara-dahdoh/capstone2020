import requests

def documentIDs(docket_id):
    api_key = 'VuyuxjcxoIuIAJkP7JuIOh7sQWTNkugxKzuYSdGu'

    url = ('https://api.data.gov/regulations/v3/documents.json?api_key={}&dktid={}')

    url = url.format(api_key,docket_id)

    response = requests.get(url)
    if response.status_code == 200:
        documents = response.json().get('documents', {})
        documentsIds = [document['documentId'] for document in documents]
        print('documents ids for docket id: ' + docket_id + '\n')
        print(documentsIds)
    else:
        print('Error: ' + str(response.status_code))

# exampel of docket id
documentIDs('EPA-HQ-OAR-2011-0028')
