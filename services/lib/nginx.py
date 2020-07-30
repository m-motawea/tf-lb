from .base import SetConfigBase, ConfigNotExist
import redis, os

class Upstream(SetConfigBase):
    def __init__(self, name):
        name = f"UPSTREAM:{name}"
        super().__init__(name)
        self.increment = False

    def add_server(self, server_ip, server_port, server_weight=100):
        self.members.append(f"{server_ip}:{server_port} weight={server_weight}")
        self.increment = True
    
    def remove_server(self, server_ip, server_port, server_weight=100):
        server_cfg = f"{server_ip}:{server_port} weight={server_weight}"
        if server_cfg in self.members:
            self.members.remove(server_cfg)
        
    def list_servers(self):
        return self.members

    def save(self):
        super().save()
        self.redis.sadd("UPSTREAMS", self.key)
        if self.increment:
            self.redis.incr("CONFIG_VERSION")


    @classmethod
    def list_upstreams(cls):
        u = cls("temp")
        if not u.redis.exists("UPSTREAMS"):
            return []
        members = u.redis.smembers("UPSTREAMS")
        return [m.decode()[len("UPSTREAM:"):] for m in members]


class Server:
    def __init__(self, name, upstream_name=None):
        self.name = name
        self.key = f"SERVER:{name}"
        self.upstream_name = upstream_name
        self._redis = None

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
    
    def save(self):
        self.redis.set(self.key, self.upstream_name)
        self.redis.sadd("SERVERS", self.key)
        self.redis.sadd("BOUND_UPSTREAMS", self.upstream_name)
        self.redis.incr("CONFIG_VERSION")

    @classmethod
    def list_servers(cls):
        s = cls("temp")
        if not s.redis.exists("SERVERS"):
            return []
        members = s.redis.smembers("SERVERS")
        return [m.decode()[len("SERVER:"):] for m in members]

    def load(self):
        if not self.redis.exists(self.key):
            raise ConfigNotExist(f"config for key {self.key} doesn't exist")
        self.upstream_name = self.redis.get(self.key).decode()

    @classmethod
    def get(cls, name):
        obj = cls(name)
        obj.load()
        return obj
        