#!/usr/bin/python
from client import Client
from daemon import Daemon
from plotting import PlotOutput
import argparse

COMMANDS = [
    "calibrate",
    "daemonize",
    "exit",
    "plot",
    "train",
    "train_ambient"
]

def calibrate(options):
    parser = argparse.ArgumentParser(prog="calibrate")
    parser.add_argument(
        "command", metavar="<command>", choices=["start", "stop"],
        help="Execute calibration command: %(choices)s")
    args = parser.parse_args(options)

    client = Client()
    client.calibrate(args.command)

def daemonize(options):
    daemon = Daemon()
    daemon.loop()

def exit(options):
    client = Client()
    client.exit()

def plot(options):
    client = Client()
    client.enable_output_capturing(True)
    try:
        def output_provider():
            return client.fetch_output()
        plot = PlotOutput(output_provider)
        plot.show()
    finally:
        client.enable_output_capturing(False)

def train(options):
    parser = argparse.ArgumentParser(prog="train")
    parser.add_argument(
        "command", metavar="<command>", choices=["start", "stop"],
        help="Execute training command: %(choices)s")
    parser.add_argument(
        "-t", "--time", metavar="<time>", type=float, default=0,
        help="Finish training in <time> seconds. Applicable only to \
            command 'start'.")
    args = parser.parse_args(options)

    client = Client()
    client.train(args.command, args.time)

def train_ambient(options):
    parser = argparse.ArgumentParser(prog="train_ambient")
    parser.add_argument(
        "command", metavar="<command>", choices=["start", "stop"],
        help="Execute training command: %(choices)s")
    args = parser.parse_args(options)

    client = Client()
    client.train_ambient(args.command)

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
