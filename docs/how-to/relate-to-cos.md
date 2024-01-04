# How to relate to COS

## Overview

This document explains the processes and practices recommended for relating the Pollen charm to the [COS-lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite) observability stack.

## Requirements

- Juju 3 installed with both a machine and k8s controller bootstrapped
- Microk8s installed with dns, hostpath-storage and metallb enabled

## Deployment

First, start by adding a new model and deploying Pollen in the machine controller:
```
juju switch localhost # Assuming the controller's name to be "localhost"
juju add-model pollendepl
juju deploy pollen --channel=edge
```
Now, deploy the Grafana-agent subordinate charm and relate it to Pollen:
```
juju deploy grafana-agent --channel=edge
juju integrate pollen grafana-agent
```
After waiting for the charms to be idle, the juju status should look like this:
```
Model       Controller  Cloud/Region         Version  SLA          Timestamp
pollendepl  localhost   localhost/localhost  3.1.6.1  unsupported  15:06:17-03:00

App            Version  Status   Scale  Charm          Channel  Rev  Exposed  Message
grafana-agent           blocked      1  grafana-agent  edge      28  no       grafana-cloud-config: off, send-remote-write: off, grafana-dashboards-provider: off, logging-consumer: off
pollen                  active       1  pollen         edge      17  no

Unit                Workload  Agent  Machine  Public address  Ports  Message
pollen/0*           active    idle   0        10.1.17.144
  grafana-agent/0*  blocked   idle            10.1.17.144            grafana-cloud-config: off, send-remote-write: off, grafana-dashboards-provider: off, logging-consumer: off

Machine  State    Address      Inst id        Base          AZ  Message
0        started  10.1.17.144  juju-b53bc3-0  ubuntu@22.04      Running
```
In order to continue, the COS-lite bundle must be deployed in the k8s controller, downloading the offers overlay first to use it later:
```
juju switch microk8s # Assuming the controller's name to be "microk8s"
curl -L https://raw.githubusercontent.com/canonical/cos-lite-bundle/main/overlays/offers-overlay.yaml -O
juju add-model cos
juju deploy cos-lite --trust --overlay ./offers-overlay.yaml
```
After waiting for all the charms to be idle, the juju status should look like this:
```
Model  Controller  Cloud/Region        Version  SLA          Timestamp
cos    microk8s    microk8s/localhost  3.1.6    unsupported  15:50:38-03:00

App           Version  Status  Scale  Charm             Channel  Rev  Address         Exposed  Message
alertmanager  0.25.0   active      1  alertmanager-k8s  stable    96  10.152.183.59   no
catalogue              active      1  catalogue-k8s     stable    31  10.152.183.120  no
grafana       9.2.1    active      1  grafana-k8s       stable    93  10.152.183.66   no
loki          2.7.4    active      1  loki-k8s          stable   105  10.152.183.240  no
prometheus    2.47.2   active      1  prometheus-k8s    stable   156  10.152.183.169  no
traefik       2.10.4   active      1  traefik-k8s       stable   166  10.0.0.3        no

Unit             Workload  Agent  Address      Ports  Message
alertmanager/0*  active    idle   10.1.194.61
catalogue/0*     active    idle   10.1.194.34
grafana/0*       active    idle   10.1.194.58
loki/0*          active    idle   10.1.194.11   
prometheus/0*    active    idle   10.1.194.35
traefik/0*       active    idle   10.1.194.6

Offer                            Application   Charm             Rev  Connected  Endpoint              Interface                Role
alertmanager-karma-dashboard     alertmanager  alertmanager-k8s  96   0/0        karma-dashboard       karma_dashboard          provider
grafana-dashboards               grafana       grafana-k8s       93   0/0        grafana-dashboard     grafana_dashboard        requirer
loki-logging                     loki          loki-k8s          105  0/0        logging               loki_push_api            provider
prometheus-receive-remote-write  prometheus    prometheus-k8s    156  0/0        receive-remote-write  prometheus_remote_write  provider
prometheus-scrape                prometheus    prometheus-k8s    156  0/0        metrics-endpoint      prometheus_scrape        requirer
```
Now, switch back to the controller model and relate the corresponding offers to the grafana-agent charm:
```
juju switch localhost
juju consume microk8s:admin/cos.prometheus-receive-remote-write
juju consume microk8s:admin/cos.grafana-dashboards
juju integrate grafana-agent prometheus-receive-remote-write
juju integrate grafana-agent grafana-dashboards
```
Juju status should show that the grafana-agent is now active instead of blocked:
```
Model       Controller  Cloud/Region         Version  SLA          Timestamp
pollendepl  localhost   localhost/localhost  3.1.6.1  unsupported  16:02:01-03:00

SAAS                             Status  Store     URL
grafana-dashboards               active  microk8s  admin/cos.grafana-dashboards
prometheus-receive-remote-write  active  microk8s  admin/cos.prometheus-receive-remote-write

App            Version  Status  Scale  Charm          Channel  Rev  Exposed  Message
grafana-agent           active      1  grafana-agent  edge      28  no       grafana-cloud-config: off, logging-consumer: off
pollen                  active      1  pollen         edge      17  no       

Unit                Workload  Agent  Machine  Public address  Ports  Message
pollen/0*           active    idle   0        10.1.17.144            
  grafana-agent/0*  active    idle            10.1.17.144            grafana-cloud-config: off, logging-consumer: off

Machine  State    Address      Inst id        Base          AZ  Message
0        started  10.1.17.144  juju-b53bc3-0  ubuntu@22.04      Running
```
Consequently, corroborate that the metrics can be seen in Prometheus by accessing the Prometheus URL given by traefik:
```
juju run traefik/0 show-proxied-endpoints
```
Then access an example metric hitting the URL of prometheus to check that it is being scraped correctly:
```
curl -s http://10.0.0.3/cos-prometheus-0/api/v1/query\?query\=pollen_http_requests_total
```
If you result looks like this:
```
{"status":"success","data":{"resultType":"vector","result":[{"metric":{"__name__":"pollen_http_requests_total","instance":"pollendepl_174a28bf-096c-4b93-8950-8aca2fb53bc3_pollen_pollen/0","job":"pollen_0_default","juju_application":"pollen","juju_model":"pollendepl","juju_model_uuid":"174a28bf-096c-4b93-8950-8aca2fb53bc3","juju_unit":"pollen/0"},"value":[1702581642.990,"0"]}]}}
```
Congratulations, you have successfully related Pollen to COS Lite.