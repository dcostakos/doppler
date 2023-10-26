#!/usr/bin/python

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION='''
module: doppler_environment
short_description: CRUD operations on Doppler Environments
description:
- Simple create/delete of environments
- Simple list of environments
author:
- Dave Costakos <dcostako@redhat.com>
options:
  project:
    description:
    - Unique identifier for the project object in Doppler
    - Default set os env DOPPLER_PROJECT
    type: str
  slug:
    description:
    - the doppler SLUG for this environment (see the API docs)
    - Default set os env DOPPLER_SLUG
    - May fall back to snake case of environment if not set
    - one of slug or environment must be set
  environment:
    description:
    - the readable doppler Environment name
    - Default set os env DOPPLER_ENVIRONMENT
    - May fall back to slug if not set
    - one of slug or environment must be set
  url:
    description:
    - the URL for the API instance of doppler
    - May default to OS Environment variable DOPPLER_URL
    type: str
    required: False
    default: https://api.doppler.com/v3
  token:
    description:
    - Authentication token for doppler
    - May default to OS Environment variable DOPPLER_TOKEN
    type: str
    required: False
  timeout:
    description:
    - Requests timeout value for url get
    type: int
    required: False
    default: 5
  state:
    description:
    - Whether the secret should exist or not
    default: present
    choices:
    - absent
    - present
    type: str
'''

EXAMPLES='''
- name: list environment in project env-project
  dcostakos.doppler.doppler_environment:
    project: 'env-project'
    list: true
    token: my_token
  register: environments

- name: create environment in project env-project
  dcostakos.doppler.doppler_environment:
    project: 'env-project'
    environment: "CI"
    slug: "ci"
    state: present
    token: my_token
  register: environment

- name: delete environment in project env-project
  dcostakos.doppler.doppler_environment:
    project: 'env-project'
    slug: 'ci'
    state: absent
    token: my_token
  register: environment
'''

RETURN='''
changed:
  description: Whether something changed in Doppler as a result of this call
  returned: success
  type: bool
  sample: true
req:
  description: details about the request that was made to dopplers' api
  returned: success
  type: str
  sample: url: https://api.doppler.com/v3/projects, method: POST, body: b'{\"name\": \"ansible-project\", \"description\": \"Project ansible-project\"}
status_code:
  description: The HTTP status code of the request
  type: int
  returned: success
  sample: 200
environment:
  description: representation of the doppler environment
  type: dict
  returned: success
  contains:
    name:
      returned: success
      description: Display name of the environment
      type: str
      sample: "Development"
    id:
      returned: success
      description: ID of the environment (usually same as slug)
      type: str
      sample: dev
    slug:
      returned: success
      description: SLUG of the environment (usually same as slug)
      type: str
      sample: dev
    project:
      returned: success
      description: Name of the project this environment is part of
      type: str
      sample: "env-project"
    created_at:
      returned: success
      description: Timestamp that the environment was created
      type: str
      sample: 2023-10-26T16:35:27.939Z
    initial_fetch_at:
      returned: success
      description: Timestamp for initial fetch (from API).  Often null
      type: str
      sample: null
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
        'project': module.params['project']
    }

def get_headers(module):
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {module.params['token']}"
    }

def list_environments(module):
    params = get_url_params(module)
    return return_if_object(
        module,
        requests.get(
            f"{module.params['url']}/environments",
            headers=get_headers(module),
            params=params,
            timeout=module.params['timeout'],
            verify=module.params['validate_certs']
        )
    )

def get_environment(module):
    params = get_url_params(module)
    params['environment'] = module.params['environment']
    return return_if_object(
        module,
        requests.get(
          f"{module.params['url']}/environments/environment",
          params=params,
          headers=get_headers(module),
          timeout=module.params['timeout'],
          verify=module.params['validate_certs']
        ),
        allow_not_found=True
    )

def create_environment(module):
    payload = get_url_params(module)
    payload['name'] = module.params['environment']
    payload['slug'] = module.params['slug']
    headers = get_headers(module)
    headers['content-type'] = "application/json"
    return return_if_object(
        module,
        requests.post(
          f"{module.params['url']}/environments",
          json=payload, headers=headers,
          timeout=module.params['timeout'],
          verify=module.params['validate_certs']
        )
    )

def delete_environment(module):
    payload = get_url_params(module)
    payload['environment'] = module.params['slug']
    headers = get_headers(module)
    headers['content-type'] = "application/json"
    return return_if_object(
        module,
        requests.delete(
            f"{module.params['url']}/environments/environment",
            json=payload, headers=headers,
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
                fallback=(env_fallback, ['DOPPLER_ENVIRONMENT'])
            ),
            slug=dict(
                type='str',
                fallback=(env_fallback, ['DOPPLER_ENVIRONMENT_SLUG'])
            ),
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
        result = list_environments(module)
        module.exit_json(**result)

    if module.params.get('environment') is None and module.params.get('slug') is None:
        module.fail_json(msg="Either environment or slug must be provided")

    if module.params.get('slug') is None:
        module.params['slug'] = toSnakeCase(module.params['environment'])

    if module.params.get('environment') is None:
        module.params['environment'] = module.params['slug']

    result = get_environment(module)
    if module.params['state'] == 'present':
        if result is None:
            result = create_environment(module)
            result['changed'] = True

    else:
        if result:
            result = delete_environment(module)
            result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
