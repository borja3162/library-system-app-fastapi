


import pytest
from unittest.mock import Mock


from library_app.external.cache import SafeCache, configure_redis_at_app_start, TTL_SECONDS






CACHE_KEY = 'key:1'
CACHE_VAL = 'abc'


@pytest.mark.asyncio 
async def test_safe_cache_with_redis_unavailable():

    redis_mock = Mock()
    redis_mock.ping.side_effect = RuntimeError("Service unavailable")

    cache = SafeCache( redis_mock)
    await configure_redis_at_app_start(cache)

    assert not cache.enabled

    await cache.set( CACHE_KEY, CACHE_VAL) 
    result = await cache.get(CACHE_KEY)
    
    assert result is None


    redis_mock.set.assert_not_called()
    redis_mock.get.assert_not_called()



@pytest.mark.asyncio 
async def test_safe_cache_with_redis_available():

    redis_mock = Mock()

    cache = SafeCache( redis_mock)

    cache.enabled=True

    await cache.set( CACHE_KEY, CACHE_VAL) 
    result = await cache.get(CACHE_KEY)
    
    


    redis_mock.set.assert_called_once_with(CACHE_KEY, CACHE_VAL, ex = TTL_SECONDS)
    redis_mock.get.assert_called_once_with(CACHE_KEY)



@pytest.mark.external
@pytest.mark.asyncio 
async def test_safe_cache_with_redis_available():

    cache = SafeCache( )

    await configure_redis_at_app_start(cache)



    await cache.set(CACHE_KEY, CACHE_VAL)

    val = await cache.get(CACHE_KEY)

    assert val == CACHE_VAL

