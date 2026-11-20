.. meta::
   :description: Discover the Pollen charm, a Juju operator that deploys and manages Pollen the entropy server.

.. vale Canonical.007-Headings-sentence-case = NO

.. _index:

Pollen operator
===============

A Juju charm deploying and managing Pollen on a machine.
Pollen is a scalable, high performance, free software (AGPL) web server, that provides small strings of entropy, over TLS-encrypted HTTPS or clear text HTTP connections.
You might think of this as ‘Entropy-as-a-Service’.

Pollen can be used by `Pollinate <https://github.com/dustinkirkland/pollinate>`_, a free software (GPLv3) script that retrieves entropy from one or more Pollen servers and seeds the local Pseudo Random Number Generator (PRNG).

Like any Juju charm, this charm supports one-line deployment, configuration, integration, scaling, and more.
This charm simplifies initial deployment and operations of Pollen on a machine, such as scaling the number of instances and clustering and more.
As such, the charm makes it easy for those looking to take control of their own entropy generation whilst keeping operations simple.

In this documentation
---------------------

.. TODO: Use the table below as a starting place.
   You don't need to include all of the rows if they're not relevant to the charm
   or if the docs don't exist. Use the vertical line symbol | to separate pages.
   
   When linking a how-to guide, use a verb to indicate an action/task. When
   linking reference or explanation material, use gerunds or nouns.

   Use "Get started" to highlight one or more tutorials. This row touches
   on the "point of entry" domain.

   For Deployment and Operations, place the most important/common use cases first.
   If there are no meaningful Day 0/1 operations, drop "Deployment" from the table.
   If there are no meaningful Day 2 operations, drop "Operations" from the table.
   These rows touch on the domain of "lifecycle".
   
   Use the "Product-specific feature" row to highlight any 
   major selling points of the charm -- what's the value proposition of this charm?

   Use the "Design" row to showcase architecture and design-related documentation
   for this charm. This row touches on the domain of "conceptual or stack layers".
   
   If possible, include a row that touches on the "quality" domain (security, performance).

   Another charm-specific row to consider is "Integrations", especially if the
   charm is meant to work in the context of a larger deployment. The "Integrations"
   row touches on the domain of "interfaces".

.. list-table::
    :header-rows: 1

    * - 
      - 
    * - Get started
      - :ref:`Guided tutorial <tutorial_index>`
    * - Operations
      - :doc:`Integrate with COS <how-to/relate-to-cos>` | :doc:`Upgrade <how-to/upgrade>`
    * - Design
      - :doc:`Architecture <reference/charm-architecture>`

How this documentation is organized
------------------------------------

This documentation uses the `Diátaxis documentation structure <https://diataxis.fr/>`_.

- The :ref:`Tutorial <tutorial_index>` takes you step-by-step through a basic deployment of the Pollen charm.
- :ref:`How-to guides <how_to_index>` assume you have basic familiarity with the Pollen charm. Learn more about setting up, using, maintaining, and contributing to this charm.
- :ref:`Reference <reference_index>` provides a guide to actions, configurations, relations, and other technical details.
- :ref:`Explanation <explanation_index>` includes topic overviews, background and context and detailed discussion.

Contributing to this documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Documentation is an important part of this project, and we take the same open-source approach
to the documentation as the code. As such, we welcome community contributions, suggestions, and
constructive feedback on our documentation.
See :doc:`How to contribute <how-to/contribute>` for more information.

If there's a particular area of documentation that you'd like to see that's missing, please 
`file a bug <https://github.com/canonical/pollen-operator/issues>`_.

Project and community
---------------------

The Pollen Operator is a member of the Ubuntu family. It's an open-source project that warmly welcomes community
projects, contributions, suggestions, fixes, and constructive feedback.

Governance and policies
^^^^^^^^^^^^^^^^^^^^^^^

- `Code of conduct <https://ubuntu.com/community/code-of-conduct>`_

Get involved
^^^^^^^^^^^^

- `Get support <https://discourse.charmhub.io/>`_
- `Join our online chat <https://matrix.to/#/#charmhub-charmdev:ubuntu.com>`_
- :doc:`Contribute <how-to/contribute>`

Thinking about using the Pollen Operator for your next project?
`Get in touch <https://matrix.to/#/#charmhub-charmdev:ubuntu.com>`_!

.. vale Canonical.013-Spell-out-numbers-below-10 = NO
.. vale Canonical.500-Repeated-words = NO

.. toctree::
    :hidden:
    :maxdepth: 1

    Tutorial <tutorial/index>
    How-to guides <how-to/index>
    Reference <reference/index>
    Explanation <explanation/index>
