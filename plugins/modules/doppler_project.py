#!/usr/bin/python

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
module: doppler_project
short_description: CRUD operations on Doppler Projets
description:
- Simple create/delete of projects
- Simple list of projects
author:
- Dave Costakos <dcostako@redhat.com>
options:
  project:
    description:
    - Unique identifier for the project object in Doppler
    - Default set os env DOPPLER_PROJECT
    type: str
  description:
    description:
    - Description for the project
    - Default set os env DOPPLER_DESCRIPTION
    type: str
    aliases:
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

# imports
import requests

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.dcostakos.doppler.plugins.module_utils.doppler_utils import (
    DopplerModule,
)

def get_url_params(module):
    return { k:module.params[k] for k in ('project') }

def get_headers(module):
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {module.params['token']}"
    }

def get_project(module):
    return return_if_object(
        module,
        requests.get(
          f"{module.params['url']}/projects/project",
          params=get_url_params(module),
          headers=get_headers(module),
          timeout=module.params['timeout']
        ),
        allow_not_found=True
    )

def create_project(module):
    return update_project(module)

def delete_project(module):
    payload = { "project": module.params['project'] }
    headers = get_headers(module)
    headers['content-type'] = "application/json"
    return_if_object(
        module,
        requests.delete(
            f"{module.params['url']}/projects/project",
            json=payload, headers=headers,
            timeout=module.params.get['timeout']
        )
    )

def update_project(module):
    payload = {
        "project": module.params['project'],
        "description": module.params['description']
    }
    headers = get_headers(module)
    headers['content-type'] = "application/json"
    return_if_object(
        module,
        requests.post(
          f"{module.params['url']}/projects/project",
          json=payload, headers=headers,
          timeout=module.params['timeout']
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
        result['url'] = response.request.url
        result['status_code'] = response.status_code
    else:
        module.fail_json(msg=f"Unexpected REST failure {response.json()}")
    return result

def run_module():
    module = DopplerModule(
        argument_spec = dict(
            project=dict(
                type='str',
                aliases=['name'],
                fallback=(env_fallback, ['DOPPLER_PROJECT']),
                required=True),
            descripton=dict(
                type='str',
                fallback=(env_fallback, ['DOPPLER_DESCRIPTION']),
                required=False),
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

    if module.params['description'] is None:
        module.params['description'] = f"Project {module.params['project']}"


    result = get_project(module)
    if module.params['state'] == 'present':
        if result is None:
            result = create_project(module)
            result['changed'] = True
        else:
            if result['project']['description'] != module.params['description']:
                result = update_project(module)
                result['changed'] = True

    else:
        if result:
            result = delete_project(module)
            result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()