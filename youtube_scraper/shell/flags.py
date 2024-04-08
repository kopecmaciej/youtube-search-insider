import argparse


class Flags:
    parser: argparse.ArgumentParser

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="Youtube Scraper")
        self.add_flags()

    def get_flags(self):
        return self.parser

    def add_flags(self):
        self.parser.add_argument("-s", "--search_phrase", type=str)
        self.parser.add_argument(
            "-ss",
            "--search_phrases",
            nargs="+",
            help="List of search phrases",
        )
        self.parser.add_argument(
            "--languages",
            type=lambda x: x.split(","),
            help="List of languages to transcript, e.g. en,es,fr",
            default=["en"],
        )

    def parse_args(self):
        return self.parser.parse_args()
