#!/usr/bin/python
from client import Client
from daemon import Daemon
import argparse

COMMANDS = [
    "daemonize",
    "exit",
    "train"
]

def daemonize(options):
    daemon = Daemon()
    daemon.loop()

def exit(options):
    client = Client()
    client.exit()

def train(options):
    parser = argparse.ArgumentParser(prog="train")
    parser.add_argument(
        "command", metavar="<command>", choices=["start", "stop"],
        help="Execute training command: %(choices)s")
    args = parser.parse_args(options)

    client = Client()
    client.train(args.command)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "command", metavar="<command>", choices=COMMANDS,
        help="Execute command: %(choices)s")
    argparser.add_argument(
        "options", metavar="<options>", nargs=argparse.REMAINDER,
        help="Command options")
    args = argparser.parse_args()
    locals()[args.command](args.options)
