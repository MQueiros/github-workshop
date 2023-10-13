import json
import jwt
import requests
import time
import sys

PATH_TO_PRIVATE_PEM = "./../mqueirosgithubapp.2023-10-13.private-key.pem"
APP_ID = "407748"

# Open PEM
with open(PATH_TO_PRIVATE_PEM, 'rb') as pem_file:
    signing_key = jwt.jwk_from_pem(pem_file.read())

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,
    # GitHub App's identifier
    'iss': APP_ID
}

# Create JWT
jwt_instance = jwt.JWT()
encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

installation_id = requests.get(
    "https://api.github.com/app/installations",
    headers={
        "Accept": "application/vnd.github.+json",
        "Authorization": f"Bearer {encoded_jwt}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)
print(installation_id.json()[0]['id'])

installation_token = requests.post(
    f"https://api.github.com/app/installations/{installation_id.json()[0]['id']}/access_tokens",
    headers={
        "Accept": "application/vnd.github.+json",
        "Authorization": f"Bearer {encoded_jwt}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)
print(installation_token.json())

#####

ISSUE_NUMBER= '2'
#AUTH_TOKEN= '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'
AUTH_TOKEN = installation_token.json()["token"]

# The repository to add this issue to
REPO_OWNER = 'MQueiros'
REPO_NAME = 'github-workshop'

def update_issue(ISSUE_NUMBER):
    url = 'https://api.github.com/repos/%s/%s/issues/%s' % (
        REPO_OWNER, REPO_NAME, ISSUE_NUMBER)

    # Create an authenticated session to create the issue
    session = requests.Session()
    # Create our issue and headers to authenticate/format
    headers = {'Authorization': 'token %s' % AUTH_TOKEN,
               'Accept': 'application/vnd.github.v3+json'}
    # Put the values you want to modify 
    issue= {
        'title': 'New issue with installation token created from create_an_issue.py',
        'labels': ['installation_token'],
    }

    # Perform the change in your repository
    r = session.patch(url, data=json.dumps(issue), headers=headers)
    if r.status_code == 200:
        print('Successfully changed Issue #{0}: {1}'.format(
            r.json().get("number"), r.json().get("title")))
    else:
        print('Could not modify Issue #{0}'.format(ISSUE_NUMBER))
        print('Response:', r.content)

update_issue(ISSUE_NUMBER)
