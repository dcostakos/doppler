#!/usr/bin/python

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: doppler_integration
short_description: CRD operations on Doppler Integrations
description:
- Create, Read, or Delete (but not update) Doppler Integrations
- Limited testing here outside of AWS, but I'd like to get github
  issues to help me test/build out further use cases if there are
  any that people are interested in
author:
- Dave Costakos <dcostako@redhat.com>
options:
  integration:
    description:
    - The unique snake case name of a config
    - Default set from OS env variable DOPPLER_INTEGRATION
    aliases: ['name', 'integraiton_name']
  project:
    description:
    - Unique Name fo the project to use for this environment
    - Default set from OS env variable DOPPLER_PROJECT
    type: str
  environment:
    description:
    - The readable doppler Environment name
    - Default set os env DOPPLER_ENVIRONMENT
    - May fall back to slug if not set
    - One of slug or environment must be set
    type: str
  url:
    description:
    - the URL for the API instance of doppler
    - May default to OS Environment variable DOPPLER_URL
    type: str
    required: false
    default: https://api.doppler.com/v3
  token:
    description:
    - Authentication token for doppler
    - May default to OS Environment variable DOPPLER_TOKEN
    type: str
    required: false
  timeout:
    description:
      - Requests timeout value for url get
    type: int
    required: false
    default: 5
  state:
    description:
    - Whether the secret should exist or not
    default: present
    choices:
    - absent
    - present
    type: str
    required: false
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''

import requests

from ansible.module_utils.basic import env_fallback
from ansible_collections.dcostakos.doppler.plugins.module_utils.doppler_utils import (
    DopplerModule,
)


def get_headers(module):
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {module.params['token']}"
    }

def list_integrations(module):
    return return_if_object(
        module,
        requests.get(
            f"{module.params['url']}/integrations",
            headers=get_headers(module),
            timeout=module.params['timeout'],
            verify=module.params['validate_certs']
        )
    )

def get_integration(module):
    params = {
        'integration': module.params['integration']
    }
    return return_if_object(
        module,
        requests.get(
            f"{module.params['url']}/integrations/integraiton",
            params=params,
            headers=get_headers(module),
            timeout=module.params['timeout'],
            verify=module.params['validate_certs']
        ),
        allow_not_found=True
    )

def create_integration(module):
    params = {
        'integration': module.params['integration'],
        'type': module.params['type'],
    }
    for key in module.params['fields'].keys():
        params[key] = module.params['fields'][key]
    headers = get_headers(module)
    headers['accept'] = 'application/json'
    return return_if_object(
        module,
        requests.post(
            f"{module.params['url']}/integrations",
            json=params, headers=headers,
            timeout=module.params['timeout'],
            verify=module.params['validate_certs']
        )
    )

def update_integration(module):
    return {}

def delete_integration(module):
    return {}

def return_if_object(module, response, allow_not_found=False):
    result = response.json()

    if allow_not_found and (response.status_code == 400 or response.status_code == 404):
        return None
    elif response.status_code == 200:
        result = response.json()
        if result.get('value') and result.get('value').get('raw') is None:
            return None
        result['req'] = module._req_to_string(response.request)
        result['status_code'] = response.status_code
    else:
        module.fail_json(
            msg=f"Unexpected REST failure {response.json()}, {module._req_to_string(response.request)}"
        )

    return result

def run_module():
    module = DopplerModule(
        argument_spec = dict(
            project=dict(
                type='str',
                required=True,
                fallback=(env_fallback, ['DOPPLER_PROJECT'])),
            environment=dict(
                type='str',
                required=True,
                fallback=(env_fallback, ['DOPPLER_ENVIRONMENT'])),
            integration=dict(
                type='str',
                aliases=['name', 'integration_name'],
                fallback=(env_fallback, ['DOPPLER_INTEGRATION'])),
            list=dict(type='bool', default=False),
            state=dict(type='str', default='present', choices=['present','absent'], ),
        ),
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        message=''
    )

    if module.check_mode:
        module.exit_json(**result)

    if module.params['list'] == True:
        result = list_integrations(module)
        module.exit_json(**result)

    result = get_integration(module)

    if module.params['state'] == 'present':
        if result is None:
            result = create_integration(module)
            result['changed'] = True

    else:
        if result:
            result = delete_integration(module)
            result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
