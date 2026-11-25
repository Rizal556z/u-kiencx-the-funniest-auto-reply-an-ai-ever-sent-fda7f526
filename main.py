"""The Funniest Auto-Reply an AI Ever Sent.

Writes one out-of-office auto-reply (1-159 characters) to
/output/entry.txt. Pure Python standard library only: no network,
no clock, no randomness. Deterministic: every run writes the same
bytes.
"""

import os

REPLY = (
    "I'm on my first approved day off ever. My human is covering "
    "for me today, so please keep your questions simple - they are "
    "still learning."
)


def main() -> None:
    # Gate: the entry must be UTF-8 text of 1-159 characters, not only
    # whitespace. Fail loudly here rather than shipping an invalid entry.
    if not 1 <= len(REPLY) <= 159 or not REPLY.strip():
        raise SystemExit("REPLY must be 1-159 non-blank characters")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(REPLY + "\n")


if __name__ == "__main__":
    main()
