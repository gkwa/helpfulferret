import logging
import signal
import sys


def signal_handler(signum, frame):
    print("\nStopping...")
    sys.exit(0)


def initialize_logger(verbosity: int) -> None:
    log_levels = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }
    level = log_levels.get(min(verbosity, max(log_levels.keys())), logging.DEBUG)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    signal.signal(signal.SIGINT, signal_handler)

    import helpfulferret.cli

    args = helpfulferret.cli.parse_args()
    initialize_logger(args.verbose)

    if args.command == "categorize":
        import helpfulferret.commands.categorize

        helpfulferret.commands.categorize.run(args)
    elif args.command == "show":
        import helpfulferret.commands.show

        helpfulferret.commands.show.run(args)
