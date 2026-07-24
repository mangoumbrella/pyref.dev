from starlette.testclient import TestClient

from pyrefdev.server import app

client = TestClient(app)


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_search_known_symbol():
    response = client.get("/is", params={"symbol": "os.path.join"})
    assert response.status_code == 200


def test_search_unknown_symbol():
    response = client.get("/is", params={"symbol": "favicon.ico"})
    assert response.status_code == 200


def test_search_lucky_redirect():
    response = client.get(
        "/is",
        params={"symbol": "os.path.join", "lucky": "true"},
        follow_redirects=False,
    )
    assert response.status_code in (302, 307)
