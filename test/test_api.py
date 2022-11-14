import aiohttp
import pytest


@pytest.mark.asyncio
async def test_get_posts():
    data = None
    async with aiohttp.request("GET", "http://127.0.0.1:8080/posts") as response:
        data = await response.read()
    assert data is not None


# @pytest.mark.asyncio
# async def test_delete_post():
#     data = None
#     async with aiohttp.request("DELETE", "http://127.0.0.1:8000/posts/1298") as response:
#         data = await response.json()
    
#     assert data["message"] == "Ok."

@pytest.mark.asyncio
async def test_delete_post_if():
    async with aiohttp.request("DELETE", "http://127.0.0.1:8080/posts/1300") as response:
        data = await response.json()
    
    assert data["detail"] == "Post not found."


@pytest.mark.asyncio
async def test_get_post():
    data = None
    async with aiohttp.request("GET", "http://127.0.0.1:8080/posts/6") as response:
        data = await response.json()
    assert data["id"] == 6
