.. meta::
   :description: A step-by-step tutorial for deploying the Pollen charm for the first time.

.. _tutorial_basic_deployment:

Deploy the Pollen charm for the first time
==========================================

Pollen is a simple HTTP server that can distribute random values called entropy which can be used to initialize secure random number generator.
In this tutorial, we will deploy Pollen in our test environment and obtains some entropy from the deployed Pollen server.

What you'll do
--------------

1. Deploy the Pollen charm
2. Obtain entropy from Pollen using Pollinate
3. Clean up the environment

What you'll need
----------------

.. vale Canonical.013-Spell-out-numbers-below-10 = NO

.. SPREAD SKIP

You will need a working station, e.g., a laptop, with AMD64 architecture. Your working station
should have at least 4 CPU cores, 8 GB of RAM, and 50 GB of disk space.

.. tip::

    You can use Multipass to create an isolated environment by running:

    .. code-block::

        multipass launch 24.04 --name charm-tutorial-vm --cpus 4 --memory 8G --disk 50G


This tutorial requires the following software to be installed on your working station
(either locally or in the Multipass VM):

- Juju 3
- LXD

Use `Concierge <https://github.com/canonical/concierge>`_ to set up Juju and
LXD:

.. code-block::

    sudo snap install --classic concierge
    sudo concierge prepare -p machine

This first command installs Concierge, and the second command uses Concierge to install
and configure Juju and LXD.

For this tutorial, Juju must be bootstrapped to a LXD machine controller.
Concierge should complete this step for you, and you can verify by checking for
``msg="Bootstrapping Juju" provider=lxd controller=concierge-lxd``
in the terminal output and by running ``juju controllers``.

If Concierge did not perform the bootstrap, run:

.. code-block::

    juju bootstrap lxd tutorial-controller


To be able to work inside the Multipass VM, log in with the following command:

.. code-block:: bash

    multipass shell charm-tutorial-vm 

.. note::

    If you're working locally, you don't need to do this step.

.. SPREAD SKIP END

Set up the environment
----------------------

To manage resources effectively and to separate this tutorial's workload from
your usual work, create a new model in the LXD controller using the following
command:

.. code-block::

    juju add-model pollen-tutorial

Deploy the charm
----------------

Deploy the Pollen charm using the ``juju deploy`` command:

.. code-block::

    juju deploy pollen --channel latest/edge

Run ``juju status`` to check the current status of the deployment.
The output should be similar to the following:

.. terminal::

    juju status

    Model            Controller  Cloud/Region         Version  SLA          Timestamp
    pollen-tutorial  lxd         localhost/localhost  3.6.28   unsupported  21:16:49+08:00

    App     Version  Status  Scale  Charm   Channel      Rev  Exposed  Message
    pollen           active      1  pollen  latest/edge   65  no

    Unit       Workload  Agent  Machine  Public address  Ports     Message
    pollen/0*  active    idle   0        10.240.160.234  8080/tcp

    Machine  State    Address         Inst id        Base          AZ           Message
    0        started  10.240.160.234  juju-9389b4-0  ubuntu@22.04  work-laptop  Running

When the status shows "Active" for the charm, the deployment is considered finished.

Obtain entropy from Pollen using Pollinate
------------------------------------------

Now you can install Pollinate, the client for the Pollen server and try it with your new test deployment.

You can install Pollinate using ``apt``:

.. code-block::

    sudo apt install pollinate

Once installed, you can use Pollinate to test the Pollen server. The Pollen address ``10.240.160.234`` used in the example can be obtained from the ``juju status`` output.


.. terminal::

    pollinate -t -s http://10.240.160.234:8080

    <13>Nov 18 13:20:43 pollinate[15489]: client sent challenge to [http://10.240.160.234:8080]
    <13>Nov 18 13:20:43 pollinate[15489]: client verified challenge/response with [http://10.240.160.234:8080]
    +�Rʤ
    ������N�좍�}�y���?��5sJ���8Q�6���k��&�����"2Yi.C9<13>Nov 18 13:20:43 pollinate[15489]: client hashed response from [http://10.240.160.234:8080]
    <13>Nov 18 13:20:43 pollinate[15489]: client successfully seeded [-]

You can learn more about the Pollen protocol (challenge/response) in the :ref:`Pollen protocol explanation <explanation_pollen_protocol>`. See the "client successfully seeded" in the output to confirm that Pollen is working normally, here we are using the test mode of Pollinate, but in real situations, Pollinate will inject the entropy obtained from the Pollen server into system's entropy pool to make it more unpredictable in a process called seeding.

Clean up the environment
------------------------

Congratulations! You successfully deployed the Pollen charm, examined its status, and obtained entropy from the charm using Pollinate.

You can clean up your environment by following this guide:
`Tear down your test environment <https://documentation.ubuntu.com/juju/3.6/howto/manage-your-juju-deployment/tear-down-your-juju-deployment-local-testing-and-development/>`_
