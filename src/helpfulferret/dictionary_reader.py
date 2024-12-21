import logging
import pathlib
import sys


class DictionaryReader:
    def __init__(self, dict_path: str = "/usr/share/dict/american-english"):
        self.logger = logging.getLogger(__name__)
        self.dict_path = pathlib.Path(dict_path)

    def read(self) -> list[str]:
        self.logger.info(f"Reading dictionary from {self.dict_path}")
        if not self.dict_path.exists():
            self.logger.error(f"Dictionary file not found: {self.dict_path}")
            sys.exit(1)
        return self.dict_path.read_text().splitlines()
