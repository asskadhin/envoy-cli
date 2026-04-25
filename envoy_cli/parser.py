"""Parser for .env files — read, write, and manipulate key-value pairs."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Optional

# Matches: KEY=VALUE, KEY="VALUE", KEY='VALUE', with optional export prefix
_ENV_LINE_RE = re.compile(
    r'^\s*(?:export\s+)?'
    r'([A-Za-z_][A-Za-z0-9_]*)'
    r'\s*=\s*'
    r'("(?:[^"\\]|\\.)*"|\x27(?:[^\x27\\]|\\.)*\x27|[^#\r\n]*)'
    r'\s*(?:#.*)?$'
)


def _strip_quotes(value: str) -> str:
    """Remove surrounding single or double quotes from a value."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        value = value[1:-1]
    return value


def parse_env_string(text: str) -> Dict[str, str]:
    """Parse a .env-formatted string into a dict of key-value pairs.

    Blank lines and comment lines (starting with #) are ignored.
    Values may be quoted with single or double quotes.
    """
    result: Dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        match = _ENV_LINE_RE.match(line)
        if match:
            key, raw_value = match.group(1), match.group(2)
            result[key] = _strip_quotes(raw_value)
    return result


def parse_env_file(path: str | Path) -> Dict[str, str]:
    """Read a .env file from *path* and return its key-value pairs."""
    content = Path(path).read_text(encoding='utf-8')
    return parse_env_string(content)


def dump_env_string(env: Dict[str, str], quote_all: bool = False) -> str:
    """Serialise a dict of key-value pairs to a .env-formatted string.

    Values that contain whitespace, quotes, or special characters are
    always double-quoted.  Pass *quote_all=True* to quote every value.
    """
    _NEEDS_QUOTE_RE = re.compile(r'[\s"\x27\\#=]')
    lines = []
    for key, value in env.items():
        if quote_all or _NEEDS_QUOTE_RE.search(value) or value == '':
            escaped = value.replace('\\', '\\\\').replace('"', '\\"')
            lines.append(f'{key}="{escaped}"')
        else:
            lines.append(f'{key}={value}')
    return '\n'.join(lines) + ('\n' if lines else '')


def write_env_file(
    env: Dict[str, str],
    path: str | Path,
    quote_all: bool = False,
) -> None:
    """Write *env* to *path* in .env format."""
    Path(path).write_text(dump_env_string(env, quote_all=quote_all), encoding='utf-8')
