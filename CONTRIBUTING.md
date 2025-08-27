# Contributing

This document explains the processes and practices recommended for contributing enhancements to the Pollen Operator.

## Overview

- Generally, before developing enhancements to this charm, you should consider [opening an issue](https://github.com/canonical/pollen-operator/issues) explaining your use case.
- If you would like to chat with us about your use-cases or proposed implementation, you can reach
  us at the [Canonical Matrix public channel](https://matrix.to/#/#charmhub-charmdev:ubuntu.com)
  or [Discourse](https://discourse.charmhub.io/).
- Familiarizing yourself with the [Charmed Operator Framework](https://juju.is/docs/sdk) library
  will help you a lot when working on new features or bug fixes.
- All enhancements require review before being merged. Code review typically examines
  - code quality
  - test coverage
  - user experience for Juju operators of this charm.
- Please help us out in ensuring easy to review branches by re-basing your pull request branch onto the `main` branch. This also avoids merge commits and creates a linear Git commit history.
- Please generate `src` documentation for every commit. See the section below for more details.

## Developing

To make contributions to this charm, you'll need a working [development setup](https://documentation.ubuntu.com/juju/3.6/howto/manage-your-deployment/).

The code for this charm can be downloaded as follows:

```
git clone https://github.com/canonical/pollen-operator
```

Make sure to install [uv](https://docs.astral.sh/uv/), for example:

```sh
sudo snap install astral-uv --classic
```

Then install `tox` with extensions, as well as a range of Python versions:

```sh
uv tool install tox --with tox-uv
uv tool update-shell
```

To create an environment for development, use:

```shell
uv sync --all-groups
source venv/bin/activate
```

### Testing

This project uses `tox` for managing test environments. There are some pre-configured environments
that can be used for linting and formatting code when you're preparing contributions to the charm:

- `tox run -e format`: Update your code according to linting rules.
- `tox run -e lint`: Code style.
- `tox run -e unit`: Unit tests.
- `tox run -e integration`: Integration tests.
- `tox`: Runs 'format', 'lint', and 'unit' environments.


## Build charm

Build the charm in this git repository using:

```shell
charmcraft pack
```

### Deploy

```bash
# Create a model
juju add-model pollen-dev
# Enable DEBUG logging
juju model-config logging-config="<root>=INFO;unit=DEBUG"
# Deploy the charm (assuming you're on amd64)
juju deploy ./pollen_ubuntu-22.04-amd64.charm
```

## Canonical contributor agreement

Canonical welcomes contributions to the Pollen Operator. Please check out our [contributor agreement](https://ubuntu.com/legal/contributors) if you're interested in contributing to the solution.
