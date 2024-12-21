import logging
import spacy
from helpfulferret.db import WordCache


class WordCollector:
    def __init__(self, nlp_model: str = "en_core_web_sm"):
        self.logger = logging.getLogger(__name__)
        self.nlp = spacy.load(nlp_model)

    def process_word(self, word: str, cache: WordCache) -> None:
        doc = self.nlp(word)
        for token in doc:
            self.logger.debug(f"Processing: {token.text} -> {token.pos_}")
            if token.pos_ in ["VERB", "ADJ", "ADV", "PROPN"]:
                cache.cache_word(token.text, token.pos_)
