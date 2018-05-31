#!/usr/bin/python

import sys
import json

from pip import main as pip_execute

from charmhelpers.core.hookenv import (
    Hooks,
    UnregisteredHookError,
    config,
    service_name,
    relation_set,
    relation_ids,
    log
)

from cinder_contexts import ThreeParSubordinateContext

hooks = Hooks()


@hooks.hook('install')
def install():
    pip_execute(['install', 'python-3parclient'])
    pip_execute(['uninstall', 'certifi', 'urllib3', 'requests'])


@hooks.hook('config-changed',
            'upgrade-charm')
def upgrade_charm():
    for rid in relation_ids('storage-backend'):
        storage_backend(rid)


@hooks.hook('storage-backend-relation-joined',
            'storage-backend-relation-changed')
def storage_backend(rel_id=None):
    relation_set(
        relation_id=rel_id,
        backend_name=config()['volume-backend-name'] or service_name(),
        subordinate_configuration=json.dumps(ThreeParSubordinateContext()())
    )


if __name__ == '__main__':
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        log('Unknown hook {} - skipping.'.format(e))
