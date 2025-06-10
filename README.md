<!-- vale Canonical.007-Headings-sentence-case = NO -->
<!-- "Operator" is part of the name -->
# Pollen Operator
<!-- vale Canonical.007-Headings-sentence-case = YES -->

A Juju charm deploying and managing Pollen on a machine. Pollen is a scalable, high performance, free software (AGPL) web server,
that provides small strings of entropy over TLS-encrypted HTTPS or clear text HTTP connections. You might think of this as ‘Entropy-as-a-Service’.

[Pollinate](https://github.com/dustinkirkland/pollinate) is a free software (GPLv3) script that retrieves entropy from one
or more Pollen servers and seeds the local Pseudo Random Number Generator (PRNG). You might think of this as
PRNG-seeding via Entropy-as-a-Service.

This charm simplifies initial deployment and operations of Pollen on a machine, such as scaling the number of instances and
clustering and more. As such, the charm makes it easy for those looking to take control of their own entropy generation
whilst keeping operations simple.

Like any Juju charm, this charm supports one-line deployment, configuration, integration, scaling, and more.
For Charmed Pollen, this includes:
  - Scaling

For information about how to deploy, integrate, and manage this charm,
see the Official [Pollen Operator Documentation](https://charmhub.io/pollen/docs).

## Get started

You can follow the tutorial [here](https://charmhub.io/pollen/docs/how-to-relate-to-cos).

You can check out the [full list of actions here](https://charmhub.io/pollen/actions).

## Integrations

This charm can be integrated with other Juju charms and services:

  - [Grafana Agent](https://charmhub.io/grafana-agent-k8s): Grafana Agent is an OpenTelemetry Collector distribution with configuration inspired by Terraform.
  - [Apache2](https://charmhub.io/apache2): The Apache HTTP Server Project is an effort to develop and maintain an open-source HTTP server for modern operating systems.

For a full list of integrations, see the [Charmhub documentation](https://charmhub.io/pollen/integrations).

## Learn more
* [Read more](https://charmhub.io/pollen) <!--Link to the charm's official documentation-->
* [Developer documentation](https://github.com/canonical/pollen) <!--Link to any developer documentation-->
* [Troubleshooting](https://matrix.to/#/#charmhub-charmdev:ubuntu.com) <!--(Optional) Link to a page or section about troubleshooting/FAQ-->

## Project and community
* [Issues](https://github.com/canonical/pollen-operator/issues) <!--Link to GitHub issues (if applicable)-->
* [Contributing](https://charmhub.io/pollen/docs/how-to-contribute) <!--Link to any contribution guides-->
* [Matrix](https://matrix.to/#/#charmhub-charmdev:ubuntu.com) <!--Link to contact info (if applicable), e.g. Matrix channel-->
