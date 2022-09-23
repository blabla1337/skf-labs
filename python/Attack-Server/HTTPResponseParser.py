# https://stackoverflow.com/questions/24728088/python-parse-http-response-string

from http.client import HTTPResponse
from io import BytesIO

class FakeSocket():
    def __init__(self, response_bytes):
        self._file = BytesIO(response_bytes)
    def makefile(self, *args, **kwargs):
        return self._file

def Parse(http_response_bytes) -> HTTPResponse:
    source = FakeSocket(http_response_bytes)
    response = HTTPResponse(source)
    response.begin()
    return response
