"""Startup script for StefParse"""
import argparse
import logging
import logging.handlers

import serial

from stefparse.parse import start_stefparse


def main():
    """Main startup argparse script"""
    parser = argparse.ArgumentParser(description="StefParse Serial Logger")

    group = parser.add_argument_group(title="Serial config")
    group.add_argument("-p", "--port", required=True,
                       help="Set the serial port to listen from")
    group.add_argument("-b", "--baudrate", default=9600,
                       help="Set the serial baudrate")
    group.add_argument("-t", "--timeout", default=0.5,
                       help="Set the timeout value for the serial "
                            "communication (default: %(default)s)")

    group = parser.add_argument_group(title="Logging config")
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose logging")
    group.add_argument("-f", "--log-dir", dest="logdir",
                       help="Enable time rotating file logging at "
                            "the path specified")
    group.add_argument("-d", "--debug", action="store_true",
                       help="Enable logging at a DEBUG level")
    args = parser.parse_args()

    # initialize logging
    handlers = list()
    if args.logdir is not None:
        handlers.append(
            logging.handlers.TimedRotatingFileHandler(
                args.logdir,
                when="D",
                interval=1,
                backupCount=45
            )
        )
    if args.verbose:
        handlers.append(logging.StreamHandler())
    if args.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )

    # initialize serial communication
    ser = serial.Serial(args.port, args.baudrate)
    ser.timeout = args.timeout

    # start serial parsing/filtering/logging
    start_stefparse(ser)


if __name__ == "__main__":
    main()
