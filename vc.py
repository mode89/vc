#!/usr/bin/python
from daemon import Daemon
import argparse

COMMANDS = ["daemonize"]

def daemonize():
    daemon = Daemon()
    daemon.loop()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "command", metavar="<command>", choices=COMMANDS,
        help="Execute command.")
    args = argparser.parse_args()
    locals()[args.command]()
