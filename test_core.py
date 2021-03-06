import core

import pytest

def test_parse_request_line():
  rline = core.RequestLine.from_string("GET /wiki/article?q=35 HTTP/1.1")
  assert rline.method == "GET"
  assert rline.target == "/wiki/article?q=35"
  assert rline.version == (1, 1)

def test_parse_space_in_target_request_line():
  with pytest.raises(core.BadRequestLineError):
    core.RequestLine.from_string("GET /wiki/russian federation HTTP/1.1")

def test_request_line_str():
  raw = "GET /wiki/article?q=35 HTTP/1.1"
  rline = core.RequestLine.from_string(raw)
  assert str(rline) == raw


def test_parse_status_line():
  sline = core.StatusLine.from_string("HTTP/1.1 200 OK")
  assert sline.version == (1, 1)
  assert sline.code == 200
  assert sline.reason == "OK"

def test_bad_status_line():
  for bad in [
    "HTTP/1.0 35x Some reason",
    "HTTP/1.1 200"
  ]:
    with pytest.raises(core.BadStatusLineError):
      core.StatusLine.from_string(bad)

def test_parse_status_line():
  raw = "HTTP/1.1 200 OK"
  sline = core.StatusLine.from_string(raw)
  assert str(sline) == raw


def test_header_line():
  header = core.Header.from_string("Date: Tue, 15 Nov 1994 08:12:31 GMT")
  assert header.name == "Date"
  assert header.value == "Tue, 15 Nov 1994 08:12:31 GMT"

def test_header_spaces_are_not_part_of_value():
  header = core.Header.from_string("Name:    Some  value  ");
  assert header.name == "Name"
  assert header.value == "Some  value"

def test_bad_headers():
  for bad in [
    "Complex name: value",
    "NoValue",
    ": empty value"
  ]:
    with pytest.raises(core.BadHeaderLineError):
      core.Header.from_string(bad)


def test_method_compare():
  assert core.Method("get") == "GET"
  assert core.Method("GET") == core.Method("get")


def test_parse_version():
  version = core.HttpVersion.from_string("HTTP/1.1")
  assert version == (1, 1)

  version = core.HttpVersion.from_string("HTTP/1.0")
  assert version == (1, 0)

def test_version_str():
  version = core.HttpVersion(1, 0)
  assert str(version) == "HTTP/1.0"

  version = core.HttpVersion(1, 1)
  assert str(version) == "HTTP/1.1"

def test_parse_bad_version():
  for bad in ["HTTP/1", "FTP/1.0", "HTTP/a.0", "HTTP/12.3", " HTTP/1.1 "]:
    with pytest.raises(Exception):
      core.HttpVersion.from_string(bad)
