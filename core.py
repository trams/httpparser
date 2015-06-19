import collections
import re

RequestLine = collections.namedtuple("RequestLine", ["method", "target", "version"])
StatusLine = collections.namedtuple("StatusLine", ["version", "code", "reason"])


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


Header = collections.namedtuple("Header", ["name", "value"])


class BadHeaderLineError(ValueError):
  pass


token_re = re.compile("^[a-zA-Z0-9!#$%&'*+-.^_`|~]+$")


def parse_header_line(line):
  try:
    name, value = line.split(":", 1)
  except ValueError:
    raise BadHeaderLineError("Unable to parse header line: expected :")
  if token_re.match(name) is None:
    raise BadHeaderLineError("Unable to parse header line: bad header name")
  value = value.strip()
  return Header(name, value)


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


HttpVersionBase = collections.namedtuple("HttpVersion", ["major", "minor"])

class HttpVersion(HttpVersionBase):
  def __new__(cls, major, minor):
    return HttpVersionBase.__new__(cls, major, minor)

  def __str__(self):
    return "HTTP/%d.%d" % (self.major, self.minor)


def parse_version(version):
  match = re.match("^HTTP/(\d).(\d)$", version)
  return HttpVersion(int(match.group(1)), int(match.group(2)))
