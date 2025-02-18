import pytest
from config import settings, Mode
import asyncio


# fix problem "different event loop"
# more about problem: https://github.com/pytest-dev/pytest-asyncio/issues/38
# https://github.com/pytest-dev/pytest-asyncio/issues/207?ysclid=lrvse25g7y347904505
@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Хранит данные в тест-сессии (аналог environment в postman)
@pytest.fixture(scope='session')
def session_storage():
    return {}