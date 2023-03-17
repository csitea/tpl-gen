from typing import List
from pydantic_yaml import YamlModel


class Peer(YamlModel):
    ip: str
    public_key: str
    description: str


class WireguardPeersModel(YamlModel):
    peers: List[Peer]
