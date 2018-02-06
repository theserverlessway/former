from __future__ import print_function
import os

import former.resource
from former.specification import CACHE_PATH


def test_former_for_every_resource():
    if os.path.exists(CACHE_PATH):
        os.remove(CACHE_PATH)

    keys = list(former.resource.SPEC['ResourceTypes'].keys())
    assert len(keys) > 0
    for idx, key in enumerate(keys):
        try:
            resource = former.resource.Resource(key)
            resource.parameters(False)
        except Exception:
            print('Failed at type %s after %s successes' % (key, idx))
            raise


def test_former_with_only_required_resources():
    resource = former.resource.Resource('AWS::IAM::Role')
    assert resource.parameters(True) == {"AssumeRolePolicyDocument": "Json - Required"}
    assert resource.parameters(False) != {"AssumeRolePolicyDocument": "Json - Required"}
