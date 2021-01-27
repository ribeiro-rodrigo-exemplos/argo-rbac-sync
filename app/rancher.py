from typing import List
import attr
import requests
from dataclasses import dataclass


@dataclass
class ClusterMembers:
    cluster_name: str
    members: List[str]


@attr.s(auto_attribs=True)
class RancherService:
    url: str
    token: str

    def list_cluster_members(self) -> List[ClusterMembers]:
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        url = f"{self.url}/v3/clusters"

        with requests.get(
            url, verify=False, headers=headers, timeout=5,
        ) as response:
            response.raise_for_status()
            return self._map_cluster_members(response.json()['data'])

    def _map_cluster_members(self, members: List[dict]) -> List[ClusterMembers]:
        pass
