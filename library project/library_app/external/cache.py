
from fastapi import Depends
import json
import logging
import redis.asyncio as redis
from typing import Annotated

from library_app.core.env_settings import EnvSettings





logger = logging.getLogger(__name__)
settings = EnvSettings()


TTL_SECONDS= 60*10
EMPTY_CACHE_VAL = "__NONE__"




class SafeCache:
    """
    Manages cache usage by wrapping redis and having helper methods that facilitate caching of Pydantic models.
    If attempts to connect to redis fail, it disables  cache

    """


    def __init__(self, redis_client = None):
        try:
            if redis_client is None:
                self.redis = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    decode_responses=True,
                    socket_connect_timeout=1,  # fast fail
                    socket_timeout=1
                )
            else:
                self.redis = redis_client
            # creating redis client object is not enough to check if redis is available.
            # later, it will be checked and updated properly on the setup method. That needs
            # async and can't be done here
            self.enabled = True

        except Exception as e:
            self.enabled = False
            self.redis = None



    async def get(self, key):
        if not self.enabled:
            return None
        try:
            result = await self.redis.get(key)
            if result  == EMPTY_CACHE_VAL:
                return None
            return result
        except Exception:
            return None

    async def set(self, key, value, ex=TTL_SECONDS):
        if not self.enabled:
            return
        try:
            if value :
                await self.redis.set(key, value, ex=ex)
            else:
                await self.redis.set(key, EMPTY_CACHE_VAL, ex=ex)
        except Exception:
            pass

    # only good for pydantic models with basic fields. It retrieves a list of
    # elements of some pydantic model serialized by the method set_pydantic_list
    async def get_pydantic_list(self, key, model_cls):
        if not self.enabled:
            return None
        try:
            print("GET   ", key)
            cached_data =await self.redis.get(key)

            ttl = await self.redis.ttl(key)
            print("cached   ", cached_data)
            print("      -  TTL", ttl)

            if cached_data is None:
                return None


            data = json.loads(cached_data)
            return [model_cls.model_validate(item) for item in data]



        except Exception as e:
            logger.exception(f"could not read cached value for key  {key}: {e}")

            return None


    # only good for pydantic models with basic fields. It stores a list of
    # elements of some pydantic model by serializing them
    async def set_pydantic_list(self, key, results, ex=TTL_SECONDS):
        if not self.enabled:
            return
        try:
            print("SET   ", key)

            json_list = [ item.model_dump(mode="json") for item in results ]
            json_data = json.dumps(  json_list )
            print( "attempt to cache   " , json_data)


            await self.redis.set(key, json_data, ex)

        except Exception as e:
            logger.exception(f"could not cache value for key  {key}: {e}")


            pass



    def get_lock(self, lock_key, time):
        if self.enabled:
            return  self.redis.lock(lock_key, timeout= time)
        return None




# common object that manages cache access across the app
_safe_cache = SafeCache()
def get_cache() -> SafeCache:
    return _safe_cache



async def configure_redis_at_app_start(cache = _safe_cache):

    #checks if redis is reachable, and if it isn't it disables cache
    if cache.redis and  cache.enabled:
        try:
            await cache.redis.ping()  # <-- forces real connection check

        except Exception as e:
            print(f"Redis unavailable, disabling cache: {e}")
            cache.enabled = False

    # sets up memory usage
    if cache.enabled :
        await cache.redis.config_set("maxmemory", "512mb")
        await cache.redis.config_set("maxmemory-policy", "allkeys-lru")





cache_dependency = Annotated[ SafeCache,  Depends(get_cache)]
