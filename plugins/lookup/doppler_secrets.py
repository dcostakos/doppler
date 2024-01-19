# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    author:
    - Dave Costakos <dcostako@redhat.com>
    module: doppler_secrets
    short_description: Get secrets from Doppler as a lookup plugin
    description:
    - retreive secrets via key name and config from doppler api
    - once a secret is retrieved, it is decoded and up to the developer to maintain the
      secrecy of the variable in which is is stored.
    - See https://docs.doppler.com/reference/secrets-get for details
    notes:
    - if you are using a version of ansible before 2.14 with the lookup plugin,
      you may get an error message that reads '_lookup() got multiple values for argument 'name'"'
    - if that is so, please try to replace 'name' with 'secretname' and see the lookup examples

    options:
        project:
            description:
            - Unique identifier for the project object in Doppler
            - Default set os env DOPPLER_PROJECT
            type: str
            required: False
        config:
            description:
            - Name of the config object in Doppler
            - example 'dev', 'prd'
            - May default to OS Environment variable DOPPLER_CONFIG
            type: str
            required: False
        secretname:
            description:
              - Name of the Doppler secret.
              - may default to OS Environment variable DOPPLER_NAME
            type: str
            required: False
            aliases: [name]
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
'''

EXAMPLES = '''
- name: Test retrieving a secret
  ansible.builtin.debug:
    msg: "{{ lookup('dcostaks.doppler.doppler_secrets',
               name='secret_name',
               config='dev',
               token=doppler_token,
               project='secret_project') }}"


- name: For versions of anisble before 2.14, 'name' may generate an error, try this
  ansible.builtin.debug:
    msg: "{{ lookup('dcostakos.doppler.doppler_secrets',
               secretname='secret_name',
               config='dev',
               token=doppler_token,
               project='secret_project') }}"
'''

RETURN = '''
    _raw:
        description: the decoded value of the secret
        type: list
        elements: str
'''

# imports
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

import os
from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError


class DopplerException(Exception):
    pass


class LookupModule(LookupBase):
    def run(self, terms=None, variables=None, **kwargs):
        if not HAS_REQUESTS:
            raise AnsibleError(
                """doppler_secrets needs the python requests library to be installed"""
            )

        self.set_options(var_options=variables, direct=kwargs)
        params = {}
        for param in ['project', 'config', 'url', 'secretname', 'token']:
            params[param] = self.get_option_with_fallback(param)

        self.validate(params)
        return [self.secret_lookup(params)]

    def secret_lookup(self, params):
        url = f"{params['url']}/configs/config/secret"
        req_params = {
            "project": params['project'],
            "config": params['config'],
            "name": params['secretname']
        }
        req_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {params['token']}"
        }
        response = requests.get(url, params=req_params, headers=req_headers,
                                timeout=self.get_option('timeout'))

        if response.status_code != 200:
            raise DopplerException(
                f"Failed to lookup secret {params} - {response.status_code} {response.text}"
            )

        return response.json()['value']['computed']

    def get_option_with_fallback(self, name, env_var=None):
        if name is None:
            raise DopplerException("in get_option_with_fallback, name cannot be None")

        val = self.get_option(name)
        if val:
            return val
        else:
            if env_var is None:
                env_var = f"DOPPLER_{name.upper()}"
            val = os.environ(env_var)
            return val

    def validate(self, params):
        for param in ['project', 'config', 'secretname', 'token', 'url']:
            if not params[param]:
                raise DopplerException(f"Unable to find configuration item {param}, cannot proceed")
        return True
