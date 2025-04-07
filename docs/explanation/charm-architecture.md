# Charm architecture

​The Pollen operator is a machine charm designed to deploy and manage Pollen directly on VMs and bare metal. [Pollen](https://github.com/dustinkirkland/pollen) is a high-performance, scalable, free web server that provides "Entropy-as-a-Service" by offering small strings of entropy over both HTTPS and clear-text HTTP connections.

This charm does not use an OCI image, as it runs directly on a machine rather than in a container. The charm uses the [pollen](https://github.com/canonical/pollen/blob/main/snap/snapcraft.yaml) [snap](https://ubuntu.com/core/docs/snaps-in-ubuntu-core) to install pollen during deployment.

Canonical provides a Pollen server as a service to the Ubuntu community at [https://entropy.ubuntu.com](https://entropy.ubuntu.com).

## Metrics

Pollen exposes the following [OTel](https://opentelemetry.io/docs/specs/otel/metrics/) compliant metrics, which are visible in Grafana after [integrating with COS](https://charmhub.io/pollen/docs/how-to-relate-to-cos).

1. **pollen_http_requests_total**: Total HTTP requests
2. **pollen_http_responses_codes**: Total HTTP requests by code
3. **pollen_system_entropy**: System entropy
4. **pollen_http_response_seconds**: HTTP response time by code
5. **pollen_response_entropy_per_byte**: Entropy per byte
6. **pollen_response_entropy_arithmetic_mean_deviation**: Entropy arithmetic mean deviation

## Juju events

For this charm, the following events are observed:

1. [install](https://documentation.ubuntu.com/juju/latest/reference/hook/index.html#install): Triggered once per unit at the beginning of a charm’s lifecycle. **Action**: Install packages and write configuration files for pollen.
2. [upgrade-charm](https://documentation.ubuntu.com/juju/latest/reference/hook/index.html#upgrade-charm): Runs once immediately after the charm directory contents have been changed by an unforced charm upgrade operation, and may do so after a forced upgrade; but will not be run after a forced upgrade from an existing error state. **Action**: Install packages and write configuration files for pollen.
3. [start](https://documentation.ubuntu.com/juju/latest/reference/hook/index.html#start): Triggered when a unit's initialization is complete. **Action**: Start the pollen service.
4. [stop](https://documentation.ubuntu.com/juju/latest/reference/hook/index.html#stop): Triggered when a Juju controller is ready to destroy the unit. **Action**: Stop the pollen service.
5. [website-relation-changed](https://documentation.ubuntu.com/juju/latest/reference/hook/index.html#endpoint-relation-changed): Emitted when another unit involved in the website relation (from either side) touches the relation data. **Action**: Updates the relation data with the website details.

See more in the Juju docs: [Hook](https://documentation.ubuntu.com/juju/latest/user/reference/hook/)

## Charm code overview

The `src/charm.py` is the default entry point for a charm and has the PollenOperatorCharm Python class which inherits from CharmBase.

CharmBase is the base class from which all Charms are formed, defined by [Ops](https://ops.readthedocs.io/en/latest/) (Python framework for developing charms).

See more information in [Ops documentation](https://juju.is/docs/sdk/ops).

The `__init__` method guarantees that the charm observes all events relevant to its operation and handles them.

Take, for example, when a configuration is changed by using the CLI.

1. User runs the configuration command:
```bash
juju config <relevant-charm-configuration>
```
2. A `config-changed` event is emitted.
3. In the `__init__` method is defined how to handle this event like this:
```python
self.framework.observe(self.on.config_changed, self._on_config_changed)
```
4. The method `_on_config_changed`, for its turn, will take the necessary actions such as waiting for all the relations to be ready and then configuring the containers.
