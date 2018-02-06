from former import specification

PRIMITIVE_TYPE = 'PrimitiveType'
PRIMITIVE_ITEM_TYPE = 'PrimitiveItemType'
TYPE = 'Type'
ITEM_TYPE = 'ItemType'
REQUIRED = 'Required'

SPEC = specification.specification()
TYPES = {}
TYPES.update(SPEC['ResourceTypes'])
TYPES.update(SPEC['PropertyTypes'])

TYPE_KEYS = {}
for key, _ in TYPES.items():
    TYPE_KEYS[key.lower()] = key


def type_key(service, type, subtype):
    if subtype:
        subtype = '.' + subtype
    return TYPE_KEYS.get(('::'.join(['AWS', service, type]) + subtype).lower())


class Resource(object):
    def __init__(self, type):
        self.root_type = type

    def parameters(self, required_only):
        root_resource = TYPES[self.root_type]

        properties = {}
        for key, value in root_resource['Properties'].items():
            prop = Property(self.root_type, key, value, required_only)
            prop_value = prop.value()
            if prop_value is None:
                print("{} {}".format(key, prop_value))
            if not required_only or prop.required():
                properties[key] = prop_value
        return properties


class Property(object):
    def __init__(self, resource, property_type, definition, required_only):
        self.resource = resource
        self.definition = definition
        self.property_type = property_type
        self.required_only = required_only

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

    def __collection_description(self):
        return "{}{}".format(self.collection_type(), ' - Required' if self.required() else '')

    def map_property(self):
        if self.is_primitive_collection():
            return {'SampleKey': self.__collection_description()}
        else:
            print(self.resource)
            print(self.item_type())
            return Resource(self.resource + '.' + self.item_type()).parameters(self.required_only)

    def list_property(self):
        if self.is_primitive_collection():
            return [self.__collection_description()]
        elif self.definition.get(ITEM_TYPE) == 'Tag':
            return [Resource('Tag').parameters(self.required_only)]
        else:
            return [self.__new_resource(self.item_type())]

    def __get_value(self, type):
        return getattr(self, type.lower() + '_property')()

    def __new_resource(self, type):
        child_type = self.resource.split('.')[0] + '.' + type

        if self.resource != child_type and 'Properties' in TYPES.get(child_type, {}):
            return Resource(child_type).parameters(self.required_only)
        elif self.resource != child_type:
            return Property(
                child_type,
                TYPES[child_type].get(ITEM_TYPE, TYPES[child_type][PRIMITIVE_TYPE]),
                TYPES[child_type]
            ).type()
        else:
            return {'Recursive': self.resource, REQUIRED: self.required()}

    def value(self):
        if self.is_primitive():
            return "{}{}".format(self.type(), ' - Required' if self.required() else '')
        elif self.is_collection():
            return self.__get_value(self.type())
        else:
            return self.__new_resource(self.type())
