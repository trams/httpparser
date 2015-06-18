import collections
import re

RequestLine = collections.namedtuple("RequestLine", ["method", "target", "version"])
StatusLine = collections.namedtuple("StatusLine", ["version", "code", "reason"])

class Method(str):
  def __new__(cls, value, distinct=False):
    upper = value.upper()
    if distinct:
      return str.__new__(cls, upper)
    else:
      if upper == "GET":
        return GET
      elif upper == "POST":
        return POST
      else:
        return str.__new__(cls, upper)

GET = Method("GET", True)
POST = Method("POST", True)

HttpVersion = collections.namedtuple("HttpVersion", ["major", "minor"])


def parse_version(version):
  match = re.match("^HTTP/(\d).(\d)$", version)
  return HttpVersion(int(match.group(1)), int(match.group(2)))


class BadRequestLineError(ValueError):
  pass

class BadStatusLineError(ValueError):
  pass


def parse_request_line(line):
  parts = line.split(" ")
  if len(parts) != 3:
    raise BadRequestLineError("Unable to parse request line")

  return RequestLine(Method(parts[0]), parts[1], parse_version(parts[2]));


def parse_status_line(line):
  parts = line.split(" ", 2)
  if len(parts) != 3:
    raise BadStatusLineError("Unable to parse status line")

  try:
    return StatusLine(parse_version(parts[0]), int(parts[1]), parts[2])
  except ValueError:
    raise BadStatusLineError("Unable to parse status line: bad status code")
