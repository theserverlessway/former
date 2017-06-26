import former.resource


def test_former_for_every_resource():
    keys = [key for key, value in former.resource.SPEC['ResourceTypes'].items()]
    assert len(keys) > 0
    print(keys)
    for key in keys:
        resource = former.resource.Resource(key)
        resource.parameters()
