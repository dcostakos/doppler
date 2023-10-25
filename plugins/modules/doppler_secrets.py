#!/usr/bin/python

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: doppler_secrets
short_description: CRUD operations on Doppler Secrets
description:
- Simple create/delete of secrets
- Simple list of secrets
- supports config/project
- API token required
author:
- Dave Costakos <dcostako@redhat.com>
options:
  project:
    description:
    - Unique identifier for the project object in Doppler
    - Default set os env DOPPLER_PROJECT
    type: str
  config:
    description:
    - Name of the config object in Doppler
    - May default to OS Environment variable DOPPLER_CONFIG
    type: str
  name:
    description:
    - Name of the Doppler secret
    - may default to OS Environment variable DOPPLER_NAME
    type: str
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
  value:
    description:
    - the value of the stored secret
    - this will be set upon create
    - this will be updated if the secret's current value is not this
    - value equates to the raw setting for the secret which may reference other secrets
    - Using references that are unable to be resolved results in an API error
    - See https://docs.doppler.com/docs/secrets#referencing-secrets
    type: str
  return_value:
    description:
    - Whether to return the value or not
    - if true (default), return the decrypted value
    - if false, do not return, useful for validating a secret exists
    type: bool
    default: True
notes:
- 'API Reference U(https://docs.doppler.com/reference/api)'
- 'Official Documentation U(https://docs.doppler.com/docs)'
'''

EXAMPLES = '''
- name: Create a new doppler secret
  dcostakos.doppler.doppler_secrets:
    name: my_secret
    project: secret_project
    config: dev
    token: my_token
    value: super_secret

- name: Validate that doppler secret exists
  dcostakos.doppler.doppler_secrets:
    name: my_secret
    project: secret_project
    config: dev
    token: my_token
    return_value: false

- name: Delete a doppler secret secret
  dcostakos.doppler.doppler_secrets:
    name: my_secret
    project: secret_project
    config: dev
    token: my_token
    state: absent

- name: Update a doppler secret
  dcostakos.doppler.doppler_secrets:
    name: my_secret
    project: secret_project
    config: dev
    token: my_token
    value: super_secret_new_value
'''

RETURN = '''
changed:
  description: Whether something changed in Doppler as a result of this call
  returned: success
  type: bool
  sample: true
name:
  description: Name of the secret created/updated
  type: str
  returned: success
  sample: my_secret
status_code:
  description: HTTP status code returned by Doppler API
  returned: success
  type: int
  sample: 200
url:
  description: the URL of the requested resource with encoded parameters
  type: str
  returned: success
  sample: https://api.doppler.com/v3/configs/config/secret?name=MY_SECRET&project=example-project&config=dev
value:
  description: Secret value information
  returned: success
  type: dict
  contains:
    computed:
      description: The dereferenced secret value
      returned: success
      type: str
      sample: my_secret_value
    raw:
      description: The referenced secret value
      returned: success
      type: str
      sample: ${SECRET_REFERENCE}
'''

# imports
import requests

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.dcostakos.doppler.plugins.module_utils.doppler_utils import (
    DopplerException,
    DopplerModule,
)


def get_url_params(module):
    return { k:module.params[k] for k in ('name','project','config') }


def get_headers(module):
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {module.params['token']}"
    }


def get_secret(module):
    return return_if_object(
        module,
        requests.get(
          f"{module.params['url']}/configs/config/secret",
          params=get_url_params(module),
          headers=get_headers(module),
          timeout=module.params['timeout']
        ),
        allow_not_found=True
    )


def create_secret(module):
    return update_secret(module)


def update_secret(module):
    payload = {
        "project": module.params['project'],
        "config": module.params['config'],
        "change_requests": [
            {
                "name": module.params['name'],
                "originalName": module.params['name'],
                "value": module.params['value']
            }
        ]
    }
    headers = get_headers(module)
    headers['Content-type'] = "application/json"
    return_if_object(
        module,
        requests.post(
          f"{module.params['url']}/configs/config/secrets",
          json=payload, headers=headers,
          timeout=module.params['timeout']
        )
    )
    return get_secret(module)


# not documented, but what the heck
def delete_secret(module):
    payload = {
        "project": module.params['project'],
        "config": module.params['config'],
        "change_requests": [
            {
                "name": module.params['name'],
                "originalName": module.params['name'],
                "value": None,
                "shouldDelete": True
            }
        ]
    }
    headers = get_headers(module)
    headers['Content-type'] = "application/json"
    return return_if_object(
        module,
        requests.post(
          f"{module.params['url']}/configs/config/secrets",
          json=payload, headers=headers,
          timeout=module.params['timeout']),
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
            name=dict(type='str', fallback=(env_fallback, ['DOPPLER_NAME'])),
            state=dict(type='str', default='present', choices=['present','absent'], ),
            value=dict(type='str'),
            return_value=dict(type='bool', default=True),
        ),
        supports_check_mode=True
    )
    result = dict(
        changed=False,
        message=''
    )

    if module.check_mode:
        module.exit_json(**result)

    result = get_secret(module)
    if module.params['state'] == 'present':
        # secret is absent
        if result is None:
            if module.params.get('value'):
                result = create_secret(module)
                result = get_secret(module)
                result['changed'] = True
            else:
                module.fail_json(
                  msg=f"Secret {module.params['name']} doesn't exist and can't create with no value"
                )
        # secret is present
        else:
            # compariing the "raw" secret rather than the calculated secret
            # seems to be what makes the most sense
            if module.params.get('value'):
                if module.params.get('value') != result['value']['raw']:
                    result = update_secret(module)
                    result['changed'] = True
            else:
                result['changed'] = False


    elif module.params['state'] == 'absent':
        if result is None:
            result = dict(
                changed=False,
                msg=f"Secret {module.params['name']} is absent"
            )
        else:
            result = delete_secret(module)
            result['changed'] = True


    if not module.params['return_value']:
        result.pop('value')
        result['note'] = "Not returning value because return_value set to false"
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
