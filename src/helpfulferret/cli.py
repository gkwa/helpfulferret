import argparse
import pathlib


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process dictionary words and identify parts of speech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
 %(prog)s categorize -v     Process words with verbose output
 %(prog)s show -v --output words.json    Export categorized words
""",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=False,
        title="commands",
        metavar="COMMAND",
        help="Command to execute",
    )

    cat_parser = subparsers.add_parser(
        "categorize",
        help="Process and categorize dictionary words",
        description="Read dictionary words and determine their parts of speech",
    )
    cat_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )
    cat_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force reprocessing of cached words",
    )

    show_parser = subparsers.add_parser(
        "show",
        help="Show categorized words",
        description="Export categorized words to JSON format",
    )
    show_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )
    show_parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("words.json"),
        help="Output JSON file path (default: words.json)",
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        parser.exit()

    return args
