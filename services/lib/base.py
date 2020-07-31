import redis
import os
import datetime

"""
this class is stored in an set in redis

"""

class ConfigNotExist(Exception):
    pass


class SetConfigBase:
    def __init__(self, key):
        self._redis = None
        self.key = key
        self.members = []

    def _log_error(self, message):
        print(f"{str(datetime.datetime.utcnow())} ERROR: {message}") # TODO add proper logging

    @staticmethod
    def _get_redis_connection():
        return redis.Redis(
            host=os.environ.get("REDIS_IP_ADDRESS", "127.0.0.1"),
            port=int(os.environ.get("REDIS_PORT", 6379)),
        )

    @property
    def redis(self):
        if not self._redis:
            self._redis = self._get_redis_connection()
        return self._redis

    def load(self):
        if not self.redis.exists(self.key):
            raise ConfigNotExist(f"config for key {self.key} doesn't exist")
        try:
            self.members = [m.decode() for m in self.redis.smembers(self.key)]
        except Exception as e:
            self._log_error(f"failed to load upstream {self.key} due to error {e}")

    def save(self):
        if self.members:
            self.redis.sadd(self.key, *self.members)

    @classmethod
    def get(cls, key):
        obj = cls(key)
        obj.load()
        return obj

    def delete(self):
        self.redis.delete(self.key)