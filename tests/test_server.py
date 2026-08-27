import pytest
from starlette.testclient import TestClient

from pyrefdev import mapping
from pyrefdev.server import app

client = TestClient(app)


@pytest.fixture(params=["sqlite", "modules"])
def backend(request, sqlite_backend, module_backend, monkeypatch):
    """Serve the endpoints from each backend in turn.

    Which one the server picks depends on whether an index has been built, so
    both are exercised explicitly rather than left to the environment.
    """
    chosen = sqlite_backend if request.param == "sqlite" else module_backend
    monkeypatch.setattr(mapping, "_backend", chosen)
    return chosen


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_search_known_symbol(backend):
    response = client.get("/is", params={"symbol": "click.Argument"})
    assert response.status_code == 200
    assert "click.Argument" in response.text


def test_search_unknown_symbol(backend):
    response = client.get("/is", params={"symbol": "favicon.ico"})
    assert response.status_code == 200


def test_search_lucky_redirect(backend):
    response = client.get(
        "/is",
        params={"symbol": "click.Argument", "lucky": "true"},
        follow_redirects=False,
    )
    assert response.status_code in (302, 307)
    assert response.headers["location"].endswith("#click.Argument")


def test_search_scoped_to_package(backend):
    response = client.get("/is", params={"symbol": "a", "package": "click"})
    assert response.status_code == 200


def test_lucky_without_a_symbol_redirects(backend):
    response = client.get("/is", params={"lucky": "true"}, follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"].startswith("http")


def test_redirect_known_symbol(backend):
    response = client.get("/click.Argument", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"].endswith("#click.Argument")


def test_redirect_is_case_insensitive(backend):
    response = client.get("/CLICK.BADPARAMETER", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"].endswith("#click.BadParameter")


def test_redirect_unknown_symbol_falls_back_to_search(backend):
    response = client.get("/nosuchsymbol", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/is?symbol=nosuchsymbol"
