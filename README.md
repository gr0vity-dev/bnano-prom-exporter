# bnano-prom for bnano.info

Forked from https://github.com/fikumikudev/nano-prom-exporter

## A simple metrics exporter for a nano-node daemon

### Requirements

- running a nano_node for beta environment
- docker & docker-compose



### PROMETHEUS GRAFANA DOCKER STACK

config .env
| Variable                    | Info                                                             |
| ------                      | --------------------------------------------------               |
| NANO_NODE_DOCKER_NETWORK    | nano_node network must be defined in your nano_node compose file | 
| RPC_HOST                    | container name of your nano_node                                 | 
| RPC_PORT                    | nano_node rpc port usually 55000 for beta network                | 
| NANO_PROM_DEBUG             | DEBUGGING : print exceptions, useful for debugging               | 

start pushing to bnano.info:

`docker-compose up -d`
