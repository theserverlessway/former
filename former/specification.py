import json

import requests


def specification():
    response = requests.get(
        'https://d1uauaxba7bl26.cloudfront.net/latest/CloudFormationResourceSpecification.json')
    response.raise_for_status()
    return json.loads(response.text)
