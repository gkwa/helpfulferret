import json

import helpfulferret.db


def run(args):
    cache = helpfulferret.db.WordCache()
    words = cache.get_all_words()

    print(f"Writing results to {args.output}")
    with open(args.output, "w") as f:
        json.dump(words, f, indent=2)
