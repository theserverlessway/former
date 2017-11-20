import os
import json

import requests

CACHE_PATH = '/tmp/former-spec.cached.json'


def specification():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH) as f:
            return json.load(f)
    response = requests.get(
        'https://d1uauaxba7bl26.cloudfront.net/latest/CloudFormationResourceSpecification.json')
    response.raise_for_status()
    with open(CACHE_PATH, 'w') as f:
        f.write(response.text)
    return json.loads(response.text)
