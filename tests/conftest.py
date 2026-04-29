import pytest


@pytest.fixture(autouse=True)
def isolated_gaia_home(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIA_HOME", str(tmp_path / "gaia-home"))
