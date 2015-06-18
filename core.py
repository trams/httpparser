import collections
import re

RequestLine = collections.namedtuple("RequestLine", ["method", "target", "version"])
StatusLine = collections.namedtuple("StatusLine", ["version", "code", "reason"])

class Method(object):
  def __init__(self, value):
    self._value = value.upper()

  def __cmp__(self, other):
    if not isinstance(other, Method):
      other = Method(other)
    if self._value == other._value:
      return 0
    elif self._value < other._value:
      return -1
    else:
      return 1

  def __repr__(self):
    return repr(self._value)


class HttpVersion(object):
  def __init__(self, major, minor):
    self.major = major
    self.minor = minor

  def __eq__(self, other):
    if isinstance(other, tuple):
      return (self.major, self.minor) == other

  def __repr__(self):
    return "HTTP/%d.%d" % (self.major, self.minor)


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
