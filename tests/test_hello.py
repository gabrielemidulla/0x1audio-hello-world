import importlib.util
import json
import os
import sys
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT.parent / "0x1audio-sdk-py" / "src"


def load_hello():
    if str(SDK) not in sys.path:
        sys.path.insert(0, str(SDK))
    spec = importlib.util.spec_from_file_location("hello", ROOT / "hello.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HelloTest(unittest.TestCase):
    def test_hello_greets_and_asks_the_cloud(self):
        hello = load_hello()
        to_worker_r, to_worker_w = os.pipe()
        from_worker_r, from_worker_w = os.pipe()
        stdin = os.fdopen(to_worker_r, "rb", buffering=0)
        stdout = os.fdopen(from_worker_w, "wb", buffering=0)
        thread = threading.Thread(
            target=hello.serve,
            kwargs={"handlers": {"hello": hello.hello}, "stdin": stdin, "stdout": stdout},
            daemon=True,
        )
        thread.start()
        os.write(to_worker_w, json.dumps({"id": 1, "type": "call", "name": "hello", "body": {"name": "Ada"}}).encode() + b"\n")

        reader = LineReader(from_worker_r)
        cloud = reader.read()
        self.assertEqual(cloud["type"], "cloud")
        self.assertEqual(cloud["path"], "/api/v1/health")
        os.write(
            to_worker_w,
            json.dumps({"id": cloud["id"], "type": "cloud-result", "status": 200, "body": {"status": "ok"}}).encode() + b"\n",
        )
        event = reader.read()
        result = reader.read()
        self.assertEqual(event, {"type": "event", "name": "greeted", "body": {"name": "Ada"}})
        self.assertEqual(result["body"], {"message": "Hello, Ada", "cloud": "ok"})
        os.close(to_worker_w)
        thread.join(timeout=2)
        stdin.close()
        stdout.close()
        os.close(from_worker_r)


class LineReader:
    def __init__(self, fd):
        self.fd = fd
        self.buffer = b""

    def read(self, timeout=2):
        import select

        while b"\n" not in self.buffer:
            ready, _, _ = select.select([self.fd], [], [], timeout)
            if not ready:
                raise TimeoutError(self.buffer)
            self.buffer += os.read(self.fd, 4096)
        line, self.buffer = self.buffer.split(b"\n", 1)
        return json.loads(line)


if __name__ == "__main__":
    unittest.main()
