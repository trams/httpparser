import core

import pytest


def test_nothing():
	pass

def test_parse_request_line():
  rline = core.parse_request_line("GET /wiki/article?q=35 HTTP/1.1")
  assert rline.method == "GET"
  assert rline.target == "/wiki/article?q=35"
  assert rline.version == (1, 1)

def test_parse_space_in_target_request_line():
  with pytest.raises():
    core.parse_request_line("GET /wiki/russian federation HTTP/1.1")
