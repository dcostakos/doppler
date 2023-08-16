# Ansible Collection - dcostakos.doppler

Ansible collection that does CRUD operations on [Doppler Secrets](https://www.doppler.com/)

Review the [Doppler REST API for Details](https://docs.doppler.com/reference/api)

## Installation
The collection uses the python requests library which should be installed.

```
pip install requests
```

## Features
- CRUD Operations on Secrets
- Lookup module for secret reads
- Anisble module for more flexibility and write/delete/update access to secrets
- Idempotency

## Modules

- `doppler_secrets`: Module for CRUD Operations on Secrets
- `doppler_secrets`: Lookup module for Read operations on secrets

## Examples: Using this module

Some examples

```yaml
 - name: Idempotent create secret with a value
    dcostakos.doppler.doppler_secrets:
      name: my_secret
      project: example-project
      config: dev
      token: "{{ doppler_token }}"
      value: "my_value"
    register: secret
```

```yaml
- name: Test lookup plugin
    ansible.builtin.debug:
      msg: "{{ lookup('dcostakos.doppler.doppler_secrets', project='example-project', token=doppler_token, config='dev', name='my_secret') }}"

```

```yaml
- name: Delete existing secret
  dcostakos.doppler.doppler_secrets:
    name: my_secret
    project: example-project
    config: dev
    token: "{{ doppler_token }}"
    state: absent
```


```yaml
- name: Just validate that a secret exists, but ignore the value
  dcostakos.doppler.doppler_secrets:
    name: secret_that_exists
    project: example-project
    config: dev
    token: "{{ doppler_token }}"
    state: present
    return_value: false
```
