"""Tiny .mo file writer for tests.

Implements the GNU MO format documented at
https://www.gnu.org/software/gettext/manual/html_node/MO-Files.html so
tests do not depend on ``msgfmt`` being on ``PATH``.
"""

from __future__ import annotations

import struct
from pathlib import Path


def write_mo(
    path: Path,
    messages: dict[str, str],
    *,
    plural_messages: dict[str, tuple[str, ...]] | None = None,
    plural_forms: str = "nplurals=2; plural=(n != 1);",
    contexts: dict[tuple[str, str], str] | None = None,
) -> None:
    """Write a binary ``.mo`` catalog at ``path``.

    ``messages`` maps source → translation (singular only).
    ``plural_messages`` maps singular → ``(plural, trans_0, trans_1, ...)``.
    ``contexts`` maps ``(context, msg)`` → translation; the key is encoded
    as ``context\\x04msg`` per GNU convention.
    """
    plural_messages = plural_messages or {}
    contexts = contexts or {}

    # Empty key holds the metadata header (gettext expects it).
    header = f"Content-Type: text/plain; charset=UTF-8\nPlural-Forms: {plural_forms}\n"
    entries: list[tuple[bytes, bytes]] = [(b"", header.encode("utf-8"))]

    for src, trans in messages.items():
        entries.append((src.encode("utf-8"), trans.encode("utf-8")))

    for sing, forms in plural_messages.items():
        # msgid is "singular\x00plural"; msgstr is forms joined by NUL.
        plural = forms[0]
        translations = forms[1:]
        key = sing.encode("utf-8") + b"\x00" + plural.encode("utf-8")
        value = b"\x00".join(t.encode("utf-8") for t in translations)
        entries.append((key, value))

    for (ctx, msg), trans in contexts.items():
        key = ctx.encode("utf-8") + b"\x04" + msg.encode("utf-8")
        entries.append((key, trans.encode("utf-8")))

    entries.sort(key=lambda kv: kv[0])

    n = len(entries)
    header_size = 7 * 4
    table_size = n * 8  # two 32-bit ints per entry (length + offset)
    keys_table = header_size
    values_table = keys_table + table_size

    # Build payload (NUL-terminated strings) after the two tables.
    payload = bytearray()
    key_index: list[tuple[int, int]] = []
    value_index: list[tuple[int, int]] = []
    payload_origin = values_table + table_size

    for key, _ in entries:
        key_index.append((len(key), payload_origin + len(payload)))
        payload += key + b"\x00"
    for _, value in entries:
        value_index.append((len(value), payload_origin + len(payload)))
        payload += value + b"\x00"

    out = bytearray()
    out += struct.pack("<I", 0x950412DE)  # magic
    out += struct.pack("<I", 0)            # format revision
    out += struct.pack("<I", n)            # message count
    out += struct.pack("<I", keys_table)   # offset to key table
    out += struct.pack("<I", values_table) # offset to value table
    out += struct.pack("<I", 0)            # hash table size (none)
    out += struct.pack("<I", 0)            # hash table offset (none)
    for length, offset in key_index:
        out += struct.pack("<II", length, offset)
    for length, offset in value_index:
        out += struct.pack("<II", length, offset)
    out += payload

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(out))
