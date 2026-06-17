import struct
import zlib

import pytest


def _minimal_png() -> bytes:
    def _chunk(tag: bytes, data: bytes) -> bytes:
        body = tag + data
        crc = struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + body + crc

    ihdr = _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    idat = _chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00"))
    iend = _chunk(b"IEND", b"")
    return b"\x89PNG\r\n\x1a\n" + ihdr + idat + iend


@pytest.fixture(autouse=True)
def cleanup_uploads():
    yield
    import shutil as _shutil

    from app.core.storage import UPLOAD_DIR as _UPLOAD_DIR

    if _UPLOAD_DIR.exists():
        _shutil.rmtree(_UPLOAD_DIR)


def test_upload_image(client, admin_headers):
    png = _minimal_png()
    r = client.post(
        "/api/v1/upload/",
        headers=admin_headers,
        files={"file": ("test.png", png, "image/png")},
    )
    assert r.status_code == 200
    data = r.json()["result"]
    assert "filename" in data
    assert data["filename"].endswith(".png")
    filename = data["filename"]
    r = client.get(f"/api/v1/upload/{filename}")
    assert r.status_code == 200
    assert r.content == png


def test_upload_requires_auth(client):
    png = _minimal_png()
    r = client.post(
        "/api/v1/upload/",
        files={"file": ("test.png", png, "image/png")},
    )
    assert r.status_code == 401


def test_upload_invalid_extension(client, admin_headers):
    r = client.post(
        "/api/v1/upload/",
        headers=admin_headers,
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert r.status_code == 400


def test_get_upload_path_traversal_rejected(client):
    for malicious in ("../pyproject.toml", "..\\pyproject.toml", "foo/../../pyproject.toml"):
        r = client.get(f"/api/v1/upload/{malicious}")
        assert r.status_code == 404, malicious


def test_get_file_path_rejects_path_separators():
    from fastapi import HTTPException

    from app.core.storage import get_file_path

    for bad in ("../secret", "a/b.png", "a\\b.png", ""):
        with pytest.raises(HTTPException) as exc:
            get_file_path(bad)
        assert exc.value.status_code == 404
