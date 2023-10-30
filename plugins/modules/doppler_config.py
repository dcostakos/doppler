#!/usr/bin/python

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: doppler_config
short_description: CRUD operations on Doppler Config objects
version_added: 2.0
description:
  - Simple CRUD operations on Doppler Configs
options:
  name:
    description:
    - The unique snake case name of a config
    - Default set from OS env variable DOPPLER_CONFIG
    aliases: ['config']
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
- name: list doppler configs in ansible-project
  dcostakos.doppler.doppler_config:
    project: 'ansible-project'
    environment: 'ci'
    list: true
    token: my_token
  register: config

- name: Create ci_config config in ci environment in ansible-project
  dcostakos.doppler.doppler_config:
    project: 'ansible-project'
    environment: 'ci'
    name: 'ci-config'
    state: present
    token: my_token
  register: config

- name: Delete ci_config config in ci environment in ansible-project
  dcostakos.doppler.doppler_config:
    project: 'ansible-project'
    environment: 'ci'
    name: 'ci-config'
    state: absent
    token: my_token
  register: config
'''

RETURN = r'''
changed:
  description: Whether something changed in Doppler as a result of this call
  returned: success
  type: bool
  sample: true
req:
  description: details about the request that was made to dopplers' api
  returned: success
  type: str
status_code:
  description: The HTTP status code of the request
  type: int
  returned: success
config:
  description: Representation of the config object
  type: dict
  returned: success
  contains:
    created_at:
      returned: success
      description: Timestamp the config was craated
      type: str
      sample: 2023-10-30T18:36:19.914Z
    initial_fetch_at:
      returned: success
      description: Timesteamp of initial fetch
      type: str
      sample: null
    last_fetch_at:
      returned: success
      description: Timestamp of last fetch
      type: str
      sample: null
    locked:
      returned: success
      description: Is the config "locked" and undeletable
      type: bool
      sample: false
    name:
      returned: success
      description: Name of the config object
      type: str
      sample: ci_config
    project:
      returned: success
      description: Name of the project in which the Config item resides
      type: str
      sample: ansible-project
    environment:
      returned: success
      description: Name of the environment in which the Config item resides
      type: str
      sample: ci
    root:
      returned: success
      description: Is the item a root config item
      type: bool
      sample: false
    slug:
      returned: success
      description: Unique ID for this config item
      type: str
      sample: 0e3540b4-5bd2-4faa-8838-1349ad315fb4
'''

# imports
import requests
import re

from ansible.module_utils.basic import env_fallback
from ansible_collections.dcostakos.doppler.plugins.module_utils.doppler_utils import (
    DopplerModule,
)

def toSnakeCase(string):
    string = re.sub(r'(?<=[a-z])(?=[A-Z])|[^a-zA-Z]', ' ', string).strip().replace(' ', '_')
    return ''.join(string.lower())

def get_url_params(module):
    return {
        'project': module.params['project'],
        'environment': module.params['environment']
    }

def get_headers(module):
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {module.params['token']}"
    }

def list_configs(module):
    params = get_url_params(module)
    return return_if_object(
        module,
        requests.get(
            f"{module.params['url']}/configs",
            headers=get_headers(module),
            params=params,
            timeout=module.params['timeout'],
            verify=module.params['validate_certs']
        )
    )

def get_config(module):
    params = get_url_params(module)
    params['config'] = module.params['name']
    return return_if_object(
        module,
        requests.get(
            f"{module.params['url']}/configs/config",
            headers=get_headers(module),
            params=params,
            timeout=module.params['timeout'],
            verify=module.params['validate_certs']
        ),
        allow_not_found=True
    )

def create_config(module):
    params = get_url_params(module)
    params['name'] = module.params['name']
    headers = get_headers(module)
    headers['content-type'] = "application/json"
    return return_if_object(
        module,
        requests.post(
            f"{module.params['url']}/configs",
            headers=headers, json=params,
            timeout=module.params['timeout'],
            verify=module.params['validate_certs']
        )
    )

def delete_config(module):
    payload = {
        'project': module.params['project'],
        'config': module.params['name']
    }
    headers = get_headers(module)
    headers['content-type'] = "application/json"
    return return_if_object(
        module,
        requests.delete(
            f"{module.params['url']}/configs/config",
            headers=headers, json=payload,
            timeout=module.params['timeout'],
            verify=module.params['validate_certs']
        )
    )

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
            name=dict(
                type='str',
                aliases=['config'],
                fallback=(env_fallback, ['DOPPLER_CONFIG'])),
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
        result = list_configs(module)
        module.exit_json(**result)

    module.params['name'] = toSnakeCase(module.params['name'])

    if module.params.get('name') is None:
        module.fail_json(msg="A config name must be provided")

    result = get_config(module)

    if module.params['state'] == 'present':
        if result is None:
            result = create_config(module)
            result['changed'] = True

    else:
        if result:
            result = delete_config(module)
            result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()