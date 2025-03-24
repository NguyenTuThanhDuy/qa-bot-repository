import logging

import redis
from redis.exceptions import ConnectionError

from src.caching.config import BaseConfig as Conf


class RedisConnector:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Initialize Redis client."""
        try:
            self.client = redis.Redis(
                host=Conf.REDIS_HOST,
                port=Conf.REDIS_PORT,
                db=Conf.REDIS_DB,
                charset="utf-8",
                decode_responses=True,
                socket_timeout=Conf.REDIS_SOCKET_TIMEOUT
            )
            # Check if the connection is successful
            if not self.client.ping():
                raise ConnectionError("Redis connection failed")
        except ConnectionError as e:
            logging.error(f"Error connecting to Redis: {e}")
            raise ConnectionError(f"Cannot connect to Redis")
        except Exception as e:
            logging.error(f"Unknown error when connecting to Redis {e}")
            raise Exception(f"Unknown error when connecting to Redis")

    def get_client(self):
        """Return the Redis client instance."""
        if self.client is None:
            self._connect()
        return self.client
