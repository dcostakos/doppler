#!/usr/bin/python

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import copy
import requests

from ansible.module_utils.basic import AnsibleModule, env_fallback

class DopplerException(Exception):
    pass


class DopplerModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        arg_spec = kwargs.get('argument_spec', {})

        kwargs['argument_spec'] = self._merge_dictionaries(
            arg_spec,
            dict(
                url=dict(type='str', fallback=(env_fallback, ['DOPPLER_URL'])),
                validate_certs=dict(type='bool', default=False),
                timeout=dict(type='int', default=5),
                token=dict(type='str', fallback=(env_fallback, ['DOOPLER_TOKEN'])),
                project=dict(type='str', fallback=(env_fallback, ['DOPPLER_PROJECT'])),
                config=dict(type='str', fallback=(env_fallback, ['DOPPLER_CONFIG']))
            )

        )

        AnsibleModule.__init__(self, *args, **kwargs)

    def raise_for_status(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail_json(
                msg=f"Doppler returned error {response.json()}",
                request={
                    "url": response.request.url,
                    "body": response.request.body,
                    "method": response.request.method
                }
            )

    def _merge_dictionaries(self, a, b):
        new = copy.deepcopy(a)
        new.update(b)
        return new
