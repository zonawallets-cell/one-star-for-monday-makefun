"""One Star for Monday — make.fun entry.

Writes one one-star review of Monday, written as if Monday were a
restaurant (at most 25 words), to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

Pure standard library only.
"""

import os

REVIEW = (
    "One star. The chef's special is Monday: reheated Sunday, served "
    "at 9 a.m., with a side of 'per my last email'."
)

MAX_CHARS = 180
MAX_WORDS = 25


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-180 chars, <=25 words,
    single line, not only whitespace, no control characters."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 180-char limit" % len(text))
    if len(text.split()) > MAX_WORDS:
        raise ValueError("entry is %d words, over the 25-word limit" % len(text.split()))
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry = validate(REVIEW)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = validate(fh.read())
    assert on_disk == entry, "entry.txt on disk differs from validated entry"
    print(entry)
    print("chars: %d, words: %d" % (len(entry), len(entry.split())))


if __name__ == "__main__":
    main()
