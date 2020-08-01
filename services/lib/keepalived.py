from .base import SetConfigBase
import copy


class KeepAlivedPeers(SetConfigBase):
    def __init__(self):
        super().__init__("PEERS")

    def add_peer(self, peer_ip):
        self.members.append(peer_ip)

    def remove_peer(self, peer_ip):
        if peer_ip in self.members:
            self.members.remove(peer_ip)

    def list_peers(self):
        return copy.copy(self.members)

    def save(self):
        super().save()
        self.redis.incr("CLUSTER_VERSION")

    @classmethod
    def get(cls):
        obj = cls()
        obj.load()
        return obj
