import logging
import pathlib
import sqlite3
import typing


class WordCache:
    def __init__(self, cache_dir: typing.Optional[pathlib.Path] = None):
        self.logger = logging.getLogger(__name__)
        if cache_dir is None:
            cache_dir = pathlib.Path.home() / ".helpfulferret"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = cache_dir / "cache.db"
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS words (
                    word TEXT PRIMARY KEY,
                    pos TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def get_pos(self, word: str) -> typing.Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT pos FROM words WHERE word = ?", (word,))
            result = cursor.fetchone()
            return result[0] if result else None

    def cache_word(self, word: str, pos: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO words (word, pos) VALUES (?, ?)", (word, pos)
            )

    def get_all_words(self) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT word, pos FROM words")
            results = cursor.fetchall()
            words_by_type = {"VERB": [], "ADJ": [], "ADV": [], "PROPN": []}
            for word, pos in results:
                if pos in words_by_type:
                    words_by_type[pos].append(word)
            return words_by_type
