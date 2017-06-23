import json


def specification():
    # https://d1uauaxba7bl26.cloudfront.net/latest/CloudFormationResourceSpecification.json

    with open('CloudFormationResourceSpecification.json') as f:
        return json.loads(f.read())
