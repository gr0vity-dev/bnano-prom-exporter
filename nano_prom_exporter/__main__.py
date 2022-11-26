"""Nano Prometheus Export to Gateway

This Script allows the user to export specific
nano_node based stats to a prometheus gateway
limiting the amount of attack surface normally
needed for exposing stats like this

This script requires
`promethues_client`
`psutil`
`requests` be installed
"""

import argparse
from datetime import datetime
import logging
import time
from socket import gethostname

from prometheus_client import CollectorRegistry, Histogram

from .config import Config
from .nanoRPC import nanoRPC
from .nanoStats import nano_nodeProcess, nanoProm
from .repeatedTimer import RepeatedTimer

logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")
# logging.getLogger("requests").setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)

def generate_runid():
    runid = str(datetime.now()).replace(" ", "_")
    return runid

parser = argparse.ArgumentParser(prog="nano_prom", description="configuration values")
parser.add_argument("--host", help='"[::1]" default\thost string', default="127.0.0.1", action="store")
parser.add_argument("--port", help='"7076" default\trpc port', default="7076", action="store")
parser.add_argument("--datapath", help='"~\\Nano" as default', default="~\\Nano\\", action="store")
parser.add_argument(
    "--push_gateway",
    help='"http://localhost:9091" prometheus push gateway',
    default="http://localhost:9091",
    action="store",
)
parser.add_argument("--hostname", help="instance name to pass to prometheus", default=gethostname(), action="store")
parser.add_argument("--interval", help="interval to sleep", default="10", action="store", type=int)
parser.add_argument("--username", help="Username for basic auth on push_gateway", default="", action="store")
parser.add_argument("--password", help="Password for basic auth on push_gateway", default="", action="store")
parser.add_argument(
    "--config_path", help="Path to config.ini \nIgnores other CLI arguments", default=None, action="store"
)
parser.add_argument("--runid", help="job name to pass to prometheus", default=generate_runid(), action="store")
parser.add_argument("--runid_prefix", help="job name to pass to prometheus", default=None, action="store")

args = parser.parse_args()
cnf = Config(args)
registry = CollectorRegistry()
rpcLatency = Histogram("nano_rpc_response", "response time from rpc calls", ["method"], registry=registry)

statsCollection = nanoRPC(cnf)
promCollection = nanoProm(cnf, registry)
process_stats = nano_nodeProcess(promCollection)

last_time = 0

def try_gather_process_stats():
    try:
        process_stats.node_process_stats()
    except Exception as e:
        logging.exception(e)


def main():
    logging.info("Starting main loop")

    stats = statsCollection.gatherStats(rpcLatency)
    
    try_gather_process_stats()

    promCollection.update(stats)
    promCollection.pushStats(registry)

    global last_time
    curr_time = time.time()
    logging.info("Finished main loop, elapsed time: %s", curr_time - last_time)
    last_time = curr_time


if __name__ == "__main__":
    # RepeatedTimer(cnf.interval, main).start()
    while True:
        try:
            main()
        except Exception as e:
            logging.exception(e)

        time.sleep(args.interval)