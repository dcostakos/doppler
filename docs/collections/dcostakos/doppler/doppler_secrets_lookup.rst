
.. Created with antsibull-docs 2.5.0

dcostakos.doppler.doppler_secrets lookup -- Get secrets from Doppler as a lookup plugin
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This lookup plugin is part of the `dcostakos.doppler collection <https://galaxy.ansible.com/ui/repo/published/dcostakos/doppler/>`_ (version 1.0.1).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install dcostakos.doppler`.

To use it in a playbook, specify: ``dcostakos.doppler.doppler_secrets``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- retreive secrets via key name and config from doppler api
- once a secret is retrieved, it is decoded and up to the developer to maintain the secrecy of the variable in which is is stored.
- See https://docs.doppler.com/reference/secrets-get for details








Keyword parameters
------------------

This describes keyword parameters of the lookup. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
examples: ``lookup('dcostakos.doppler.doppler_secrets', key1=value1, key2=value2, ...)`` and ``query('dcostakos.doppler.doppler_secrets', key1=value1, key2=value2, ...)``

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config"></div>
      <p style="display: inline;"><strong>config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Name of the config object in Doppler</p>
      <p>example &#x27;dev&#x27;, &#x27;prd&#x27;</p>
      <p>May default to OS Environment variable DOPPLER_CONFIG</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-name"></div>
      <p style="display: inline;"><strong>name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Name of the Doppler secret.</p>
      <p>may default to OS Environment variable DOPPLER_NAME</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-project"></div>
      <p style="display: inline;"><strong>project</strong></p>
      <a class="ansibleOptionLink" href="#parameter-project" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Unique identifier for the project object in Doppler</p>
      <p>Default set os env DOPPLER_PROJECT</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-timeout"></div>
      <p style="display: inline;"><strong>timeout</strong></p>
      <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>Requests timeout value for url get</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">5</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-token"></div>
      <p style="display: inline;"><strong>token</strong></p>
      <a class="ansibleOptionLink" href="#parameter-token" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Authentication token for doppler</p>
      <p>May default to OS Environment variable DOPPLER_TOKEN</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-url"></div>
      <p style="display: inline;"><strong>url</strong></p>
      <a class="ansibleOptionLink" href="#parameter-url" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>the URL for the API instance of doppler</p>
      <p>May default to OS Environment variable DOPPLER_URL</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;https://api.doppler.com/v3&#34;</code></p>
    </td>
  </tr>
  </tbody>
  </table>






Examples
--------

.. code-block:: yaml

    
    - name: Test retrieving a secret
      ansible.builtin.debug:
        msg: "{{ lookup('dcostaks.doppler.doppler_secrets',
                 name='secret_name',
                 config='dev',
                 token=doppler_token,
                 project='secret_project') }}"





Return Value
------------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-_raw"></div>
      <p style="display: inline;"><strong>Return value</strong></p>
      <a class="ansibleOptionLink" href="#return-_raw" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>the decoded value of the secret</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Dave Costakos 


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/dcostakos/doppler/issues>`__
* `Repository (Sources) <https://github.com/dcostakos/doppler>`__

