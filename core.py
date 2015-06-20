import collections
import re

RequestLineBase = collections.namedtuple("RequestLine", ["method", "target", "version"])

class BadRequestLineError(ValueError):
  pass

class RequestLine(RequestLineBase):
  def __new__(cls, *args):
    return RequestLineBase.__new__(cls, *args)

  @staticmethod
  def from_string(line):
    parts = line.split(" ")
    if len(parts) != 3:
      raise BadRequestLineError("Unable to parse request line")

    return RequestLine(
      Method(parts[0]),
      parts[1],
      HttpVersion.from_string(parts[2]));

  def __str__(self):
    return " ".join([str(item) for item in self])


StatusLineBase = collections.namedtuple("StatusLine", ["version", "code", "reason"])

class BadStatusLineError(ValueError):
  pass

class StatusLine(StatusLineBase):
  def __new__(cls, *args):
    return StatusLineBase.__new__(cls, *args)

  @staticmethod
  def from_string(line):
    parts = line.split(" ", 2)
    if len(parts) != 3:
      raise BadStatusLineError("Unable to parse status line")

    try:
      return StatusLine(
        HttpVersion.from_string(parts[0]),
        int(parts[1]),
        parts[2])
    except ValueError:
      raise BadStatusLineError("Unable to parse status line: bad status code")

  def __str__(self):
    return " ".join([str(item) for item in self])


HeaderBase = collections.namedtuple("Header", ["name", "value"])

class BadHeaderLineError(ValueError):
  pass

token_re = re.compile("^[a-zA-Z0-9!#$%&'*+-.^_`|~]+$")

class Header(HeaderBase):
  def __new__(cls, *args):
    return HeaderBase.__new__(cls, *args)

  @staticmethod
  def from_string(line):
    try:
      name, value = line.split(":", 1)
    except ValueError:
      raise BadHeaderLineError("Unable to parse header line: expected :")
    if token_re.match(name) is None:
      raise BadHeaderLineError("Unable to parse header line: bad header name")
    value = value.strip()
    return Header(name, value)

  def __str__(self):
    return "%s: %s" % (self.name, self.value)


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
  content_re = re.compile("^HTTP/(\d).(\d)$")

  def __new__(cls, major, minor):
    return HttpVersionBase.__new__(cls, major, minor)

  @staticmethod
  def from_string(version):
    match = HttpVersion.content_re.match(version)
    return HttpVersion(int(match.group(1)), int(match.group(2)))

  def __str__(self):
    return "HTTP/%d.%d" % (self.major, self.minor)
