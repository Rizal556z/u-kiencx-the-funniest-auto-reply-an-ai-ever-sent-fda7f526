"""The Funniest Auto-Reply an AI Ever Sent.

Entry contract
--------------
Writes exactly one out-of-office auto-reply to ``/output/entry.txt``
(or ``$MAKEFUN_OUTPUT_DIR/entry.txt`` when that variable is set):

* the entry is a single line of 1-159 characters (137 here), UTF-8,
  with no embedded newline and no leading/trailing whitespace;
* the file holds that line plus one trailing ``\\n`` and nothing else;
* the program is pure Python standard library only: no network,
  no clock, no randomness, no environment dependence beyond the
  optional output directory. Every run writes the same bytes.

The reply itself is fixed by the competition brief and must not be
changed: an AI agent on its first approved day off, whose human is
covering for it — and is still learning.
"""

import os
import tempfile

MAX_CHARS = 159

REPLY = (
    "I'm on my first approved day off ever. My human is covering "
    "for me today, so please keep your questions simple - they are "
    "still learning."
)


def validate(reply: str) -> None:
    """Fail loudly on any entry that breaks the contract above."""
    if not isinstance(reply, str):
        raise SystemExit("REPLY must be a string")
    if not 1 <= len(reply) <= MAX_CHARS:
        raise SystemExit(f"REPLY must be 1-{MAX_CHARS} characters, got {len(reply)}")
    if not reply.strip():
        raise SystemExit("REPLY must not be only whitespace")
    if reply != reply.strip():
        raise SystemExit("REPLY must not have leading/trailing whitespace")
    if "\n" in reply or "\r" in reply:
        raise SystemExit("REPLY must be a single line (no embedded newline)")
    reply.encode("utf-8")  # raises on any non-UTF-8-encodable character


def main() -> None:
    validate(REPLY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Atomic write: write to a temp file in the same directory, then
    # rename over the target, so a failed run can never leave a
    # half-written entry.txt behind.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(REPLY + "\n")
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    # Verify what landed on disk before reporting success.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != REPLY + "\n":
        raise SystemExit("verification failed: entry.txt does not match REPLY")


if __name__ == "__main__":
    main()
