import argparse

import yaml

import former.resource
from former.resource import Resource


def arguments():
    parser = argparse.ArgumentParser(description='Print CloudFormation Resources')
    parser.add_argument('service')
    parser.add_argument('type')

    return parser.parse_args()


def main():
    args = arguments()

    type = former.resource.type_key(args.service, args.type)
    resource = Resource(type)
    cf_resource = {
        'Type': type
    }

    cf_resource['Parameters'] = resource.parameters()

    print(yaml.dump({''.join(e for e in type if e.isalnum()): cf_resource}, default_flow_style=False))
