import logging
from helpfulferret.word_collector import WordCollector
from helpfulferret.dictionary_reader import DictionaryReader
from helpfulferret.db import WordCache


def run(args):
    logger = logging.getLogger(__name__)
    reader = DictionaryReader()
    collector = WordCollector()
    cache = WordCache()

    words = reader.read()
    for word in words:
        cached_pos = cache.get_pos(word)
        if cached_pos:
            if args.verbose >= 2:
                logger.debug(f"Skipping cached word: {word} -> {cached_pos}")
            continue

        collector.process_word(word, cache)
