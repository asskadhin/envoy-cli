"""Tests for envoy_cli.parser."""

import textwrap
from pathlib import Path

import pytest

from envoy_cli.parser import (
    dump_env_string,
    parse_env_file,
    parse_env_string,
    write_env_file,
)


# ---------------------------------------------------------------------------
# parse_env_string
# ---------------------------------------------------------------------------

def test_parse_simple_pairs():
    text = "DB_HOST=localhost\nDB_PORT=5432\n"
    assert parse_env_string(text) == {'DB_HOST': 'localhost', 'DB_PORT': '5432'}


def test_parse_ignores_comments_and_blank_lines():
    text = textwrap.dedent("""
        # This is a comment
        APP_ENV=production

        # Another comment
        DEBUG=false
    """)
    result = parse_env_string(text)
    assert result == {'APP_ENV': 'production', 'DEBUG': 'false'}


def test_parse_double_quoted_value():
    result = parse_env_string('GREETING="Hello, World!"')
    assert result['GREETING'] == 'Hello, World!'


def test_parse_single_quoted_value():
    result = parse_env_string("SECRET='my secret value'")
    assert result['SECRET'] == 'my secret value'


def test_parse_export_prefix():
    result = parse_env_string('export API_KEY=abc123')
    assert result['API_KEY'] == 'abc123'


def test_parse_empty_value():
    result = parse_env_string('EMPTY=')
    assert result['EMPTY'] == ''


def test_parse_inline_comment_ignored():
    result = parse_env_string('PORT=8080 # default port')
    assert result['PORT'] == '8080'


# ---------------------------------------------------------------------------
# dump_env_string
# ---------------------------------------------------------------------------

def test_dump_simple_pairs():
    env = {'KEY': 'value'}
    assert dump_env_string(env) == 'KEY=value\n'


def test_dump_quotes_values_with_spaces():
    env = {'MSG': 'hello world'}
    output = dump_env_string(env)
    assert 'MSG="hello world"' in output


def test_dump_quote_all_flag():
    env = {'K': 'v'}
    output = dump_env_string(env, quote_all=True)
    assert output == 'K="v"\n'


def test_dump_roundtrip():
    original = {'HOST': 'localhost', 'PORT': '5432', 'DSN': 'postgres://user:pass@host/db'}
    text = dump_env_string(original)
    restored = parse_env_string(text)
    assert restored == original


# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------

def test_write_and_parse_env_file(tmp_path: Path):
    env_file = tmp_path / '.env'
    data = {'APP': 'envoy', 'VERSION': '1.0.0'}
    write_env_file(data, env_file)
    assert env_file.exists()
    loaded = parse_env_file(env_file)
    assert loaded == data
