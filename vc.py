#!/usr/bin/python
from client import Client
from daemon import Daemon
import argparse

COMMANDS = [
    "daemonize",
    "exit"
]

def daemonize():
    daemon = Daemon()
    daemon.loop()

def sendCommand(command, options):
    client = Client()
    client.sendCommand(command, options)
    client.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "command", metavar="<command>", choices=COMMANDS,
        help="Execute command.")
    argparser.add_argument(
        "options", metavar="<options>", nargs=argparse.REMAINDER,
        help="Command options")
    args = argparser.parse_args()

    if args.command == "daemonize":
        daemonize()
    else:
        sendCommand(args.command, args.options)
