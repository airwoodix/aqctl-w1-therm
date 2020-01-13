import sys
import argparse
import logging
import asyncio

from .driver import SysFSW1Therm
from sipyco.pc_rpc import simple_server_loop
from sipyco import common_args


DEFAULT_PORT = 3280


def get_argparser():
    parser = argparse.ArgumentParser(
        description="ARTIQ controller for sysfs w1 thermometers")
    common_args.simple_network_args(parser, DEFAULT_PORT)

    parser.add_argument("-d", "--device", default="w1_bus_master1",
                        help="sysFS w1 master name")

    common_args.verbosity_args(parser)
    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)

    dev = SysFSW1Therm(args.device)
    asyncio.get_event_loop().run_until_complete(dev.setup())

    simple_server_loop(
        {"w1_therm": dev}, common_args.bind_address_from_args(args), args.port)


if __name__ == "__main__":
    main()
