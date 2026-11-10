import tempfile
from pathlib import Path
from urllib.error import URLError
from unvibecode.client import Client

class FakeResponse:
    def __init__(self):
        self.calls = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, size=-1):
        self.calls += 1
        if self.calls == 1:
            return b"partial download"
        raise URLError("Simulated connection interruption")

class FakeOpener:
    def open(self, request, timeout=120):
        return FakeResponse()

with tempfile.TemporaryDirectory() as folder:
    destination = Path(folder) / "report.zip"
    destination.write_bytes(b"previous complete report")

    client = Client(url="https://example.com", token="test")
    client.opener = FakeOpener()

    try:
        client.request("/download", destination=destination)
    except RuntimeError as error:
        print("Download error:", error)

    print("Final destination contents:", destination.read_bytes())
