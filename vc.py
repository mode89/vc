#!/usr/bin/python
from client import Client
from daemon import Daemon
import argparse

COMMANDS = [
    "daemonize",
    "exit"
]

def daemonize(options):
    daemon = Daemon()
    daemon.loop()

def exit(options):
    client = Client()
    client.exit()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "command", metavar="<command>", choices=COMMANDS,
        help="Execute command.")
    argparser.add_argument(
        "options", metavar="<options>", nargs=argparse.REMAINDER,
        help="Command options")
    args = argparser.parse_args()
    locals()[args.command](args.options)
