import pytest

@pytest.mark.anyio
async def test_read_main(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Sign in" in response.text


