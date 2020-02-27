import os
import json
import platform
import pathlib

import requests

if platform.system() == 'Windows':
    CACHE_PATH = pathlib.WindowsPath(os.getenv('TEMP') + '/former-spec.cached.json')
else:
    CACHE_PATH = pathlib.Path('/tmp/former-spec.cached.json')


def specification():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH) as f:
            return json.load(f)
    response = requests.get(
        'https://d1uauaxba7bl26.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json')
    response.raise_for_status()
    with open(CACHE_PATH, 'w') as f:
        f.write(response.text)
    return json.loads(response.text)
