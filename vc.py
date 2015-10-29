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
    argparser.add_argument(
        "options", metavar="<options>", nargs=argparse.REMAINDER,
        help="Command options")
    args = argparser.parse_args()
    locals()[args.command]()
