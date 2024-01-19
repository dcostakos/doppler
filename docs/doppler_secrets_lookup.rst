
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.5.0

.. Anchors

.. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup:

.. Anchors: short name for ansible.builtin

.. Title

dcostakos.doppler.doppler_secrets lookup -- Get secrets from Doppler as a lookup plugin
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This lookup plugin is part of the `dcostakos.doppler collection <https://galaxy.ansible.com/ui/repo/published/dcostakos/doppler/>`_ (version 1.0.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install dcostakos.doppler`.

    To use it in a playbook, specify: :code:`dcostakos.doppler.doppler_secrets`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- retreive secrets via key name and config from doppler api
- once a secret is retrieved, it is decoded and up to the developer to maintain the secrecy of the variable in which is is stored.
- See https://docs.doppler.com/reference/secrets-get for details


.. Aliases


.. Requirements






.. Options

Keyword parameters
------------------

This describes keyword parameters of the lookup. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
examples: ``lookup('dcostakos.doppler.doppler_secrets', key1=value1, key2=value2, ...)`` and ``query('dcostakos.doppler.doppler_secrets', key1=value1, key2=value2, ...)``

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-config"></div>

      .. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup__parameter-config:

      .. rst-class:: ansible-option-title

      **config**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-config" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the config object in Doppler

      example 'dev', 'prd'

      May default to OS Environment variable DOPPLER\_CONFIG


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-project"></div>

      .. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup__parameter-project:

      .. rst-class:: ansible-option-title

      **project**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-project" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Unique identifier for the project object in Doppler

      Default set os env DOPPLER\_PROJECT


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-secretname"></div>
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup__parameter-name:
      .. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup__parameter-secretname:

      .. rst-class:: ansible-option-title

      **secretname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-secretname" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: name`

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the Doppler secret.

      may default to OS Environment variable DOPPLER\_NAME


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-timeout"></div>

      .. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup__parameter-timeout:

      .. rst-class:: ansible-option-title

      **timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Requests timeout value for url get


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`5`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup__parameter-token:

      .. rst-class:: ansible-option-title

      **token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-token" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Authentication token for doppler

      May default to OS Environment variable DOPPLER\_TOKEN


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-url"></div>

      .. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup__parameter-url:

      .. rst-class:: ansible-option-title

      **url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-url" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      the URL for the API instance of doppler

      May default to OS Environment variable DOPPLER\_URL


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"https://api.doppler.com/v3"`

      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - if you are using a version of ansible before 2.14 with the lookup plugin, you may get an error message that reads '\_lookup() got multiple values for argument 'name'"'
   - if that is so, please try to replace 'name' with 'secretname' and see the lookup examples

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
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




.. Facts


.. Return values

Return Value
------------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-_raw"></div>

      .. _ansible_collections.dcostakos.doppler.doppler_secrets_lookup__return-_raw:

      .. rst-class:: ansible-option-title

      **Return value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-_raw" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      the decoded value of the secret


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Dave Costakos 


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/dcostakos/doppler/issues"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/dcostakos/doppler"
    external: true


.. Parsing errors

