import argparse
import sys

import yaml

import former.resource
from former.resource import Resource


def arguments():
    parser = argparse.ArgumentParser(description='Print CloudFormation Resources')
    parser.add_argument('service')
    parser.add_argument('type')
    parser.add_argument('subtype', default='', nargs='?')

    return parser.parse_args()


def main():
    args = arguments()

    type = former.resource.type_key(args.service, args.type, args.subtype)
    if type:
        resource = Resource(type)
        cf_resource = {'Type': type}

        cf_resource['Parameters'] = resource.parameters()

        print(yaml.dump({''.join(e for e in type if e.isalnum()): cf_resource}, default_flow_style=False))
    else:
        print('Resource not found for: {} {} {}'.format(args.service, args.type, args.subtype))
        sys.exit(1)
