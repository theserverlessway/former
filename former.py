import argparse
import json
from datetime import datetime

import yaml

PRIMITIVE_TYPE = 'PrimitiveType'
PRIMITIVE_ITEM_TYPE = 'PrimitiveItemType'
TYPE = 'Type'
ITEM_TYPE = 'ItemType'
REQUIRED = 'Required'

with open('CloudFormationResourceSpecification.json') as f:
    spec = json.loads(f.read())


def arguments():
    parser = argparse.ArgumentParser(description='Print CloudFormation Resources')
    parser.add_argument('service')
    parser.add_argument('type')

    return parser.parse_args()


args = arguments()

resource_types = spec['ResourceTypes']
property_types = spec['PropertyTypes']


def resource_key(service, type):
    return resource_keys['::'.join(['AWS', service, type]).lower()]


def property_key(service, type, property):
    return property_keys[('::'.join(['AWS', service, type]) + property).lower()]


resource_keys = {}
for key, _ in resource_types.items():
    resource_keys[key.lower()] = key

property_keys = {}
for key, _ in property_types.items():
    property_keys[key.lower()] = key


class Property(object):
    def __init__(self, resource, property_type, definition):
        self.resource = resource
        self.definition = definition
        self.property_type = property_type

    def required(self):
        return self.definition['Required']

    def type(self):
        return self.definition.get(PRIMITIVE_TYPE) or self.definition[TYPE]

    def item_type(self):
        return self.definition[ITEM_TYPE]

    def collection_type(self):
        return self.definition.get(ITEM_TYPE) or self.definition[PRIMITIVE_ITEM_TYPE]

    def is_primitive(self):
        return PRIMITIVE_TYPE in self.definition or self.definition.get(TYPE) in ['Json']

    def is_collection(self):
        return self.definition.get(TYPE) in ['List', 'Map']

    def is_primitive_collection(self):
        return PRIMITIVE_ITEM_TYPE in self.definition or self.definition.get(ITEM_TYPE) in ['Json']

    def string_property(self):
        return "Required={}".format(self.required())

    def integer_property(self):
        return (100 if self.required() else -100)

    def boolean_property(self):
        return self.required()

    def double_property(self):
        return (100.5 if self.required() else -100.5)

    def long_property(self):
        return (10000 if self.required() else -10000)

    def timestamp_property(self):
        return str(datetime.today())

    def tag_property(self):
        return {
            "Key": REQUIRED,
            "Value": self.required()
        }

    def json_property(self):
        return {
            REQUIRED: self.required()
        }

    def map_property(self):
        if self.is_primitive_collection():
            return {'SampleKey': self.__get_value(self.collection_type())}
        else:
            return Resource(self.resource,
                            property_types[self.resource + '.' + self.item_type()]).parameters()

    def list_property(self):
        if self.is_primitive_collection():
            return [self.__get_value(self.collection_type())]
        elif self.definition.get(ITEM_TYPE) == 'Tag':
            return [Resource('Tag', property_types['Tag']).parameters()]
        else:
            return [self.__new_resource(self.item_type())]

    def __get_value(self, type):
        return getattr(self, type.lower() + '_property')()

    def __new_resource(self, type):
        child_type = self.resource.split('.')[0] + '.' + type
        if self.resource != child_type:
            return Resource(child_type, property_types[child_type]).parameters()
        else:
            return {'Recursive': self.resource, REQUIRED: self.required()}

    def value(self):
        if self.is_primitive() or self.is_collection():
            return self.__get_value(self.type())
        else:
            return self.__new_resource(self.type())


class Resource(object):
    def __init__(self, resource, definition):
        self.resource = resource
        self.definition = definition

    def parameters(self):
        properties = {}
        for key, value in self.definition['Properties'].items():
            prop = Property(self.resource, key, value)
            prop_value = prop.value()
            if prop_value is None:
                print("{} {}".format(key, prop_value))
            properties[key] = prop_value
        return properties


root_type = resource_key(args.service, args.type)
root_resource = resource_types[root_type]

cf_resource = {
    'Type': root_type
}

cf_resource['Parameters'] = Resource(root_type, root_resource).parameters()

for name, definition in resource_types.items():
    Resource(name, definition).parameters()

print(yaml.dump({''.join(e for e in root_type if e.isalnum()): cf_resource}, default_flow_style=False))
