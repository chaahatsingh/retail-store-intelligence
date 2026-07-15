from pathlib import Path
import json

OUTPUT_DIR = Path("output")


def load_json(filename):

    path = OUTPUT_DIR / filename

    with open(path) as f:
        return json.load(f)


def load_events():

    events = []

    with open(OUTPUT_DIR / "generated_events.jsonl") as f:

        for line in f:

            line = line.strip()

            if line:

                events.append(json.loads(line))

    return events