"""Rejected Olympic Sports — make.fun entry.

Writes one funny single-line sport the Olympics turned down to
/output/entry.txt. Python 3.13 standard library only; no network, no
randomness, no clock, no reads of any other file.

Gate (RULES.txt): the output must be UTF-8 text of 1 to 200 characters,
not only white space. The gate is enforced here, in validate_entry(),
before anything is written: an invalid text exits non-zero and writes
no file.
"""

import os
import sys

MAX_CHARS = 200
MIN_CHARS = 1
DEFAULT_OUTPUT_PATH = "/output/entry.txt"

# One line, 128 characters. A broadcast-plausible event name, a concrete
# absurd detail, and the twist landing on the last clause: the gold goes
# to whoever complains the least.
ENTRY_TEXT = (
    "Synchronised queueing: four athletes stand in a perfectly straight "
    "line for six hours; gold goes to whoever complains the least."
)


def validate_entry(text):
    """Check one candidate line against the gate.

    Returns the text unchanged when it passes. Raises TypeError when the
    input is not a str, ValueError with a plain reason otherwise.
    """
    if not isinstance(text, str):
        raise TypeError(
            "entry must be a str, got %s" % type(text).__name__)
    if len(text) < MIN_CHARS:
        raise ValueError("entry is empty (gate needs 1-200 characters)")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the 200-character gate"
            % len(text))
    if not text.strip():
        raise ValueError("entry is only white space")
    for ch in text:
        code = ord(ch)
        if code < 32 or code == 127:
            raise ValueError(
                "entry contains control character U+%04X" % code)
    return text


def write_entry(text, path):
    """Validate, then write the text as UTF-8 with no trailing newline.

    Nothing is written when validation fails: the gate check runs first,
    so an invalid entry can never leave a bad file behind.
    """
    checked = validate_entry(text)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(checked)


def main(output_path=DEFAULT_OUTPUT_PATH):
    """Write ENTRY_TEXT to output_path. Returns 0 on success, 1 on failure."""
    try:
        write_entry(ENTRY_TEXT, output_path)
    except (TypeError, ValueError, OSError) as exc:
        print("error: refusing to write entry: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

