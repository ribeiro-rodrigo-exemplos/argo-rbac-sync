from typing import List
import attr
import requests
from app.model.entities import Cluster, ClusterRoleBinding


@attr.s(auto_attribs=True)
class RancherService:
    url: str
    token: str
    timeout: int = 5

    def __attrs_post_init__(self):
        self._headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def list_clusters(self) -> List[Cluster]:

        filters = {'state': 'active'}

        url = f"{self.url}/v3/clusters"

        with requests.get(
            url, verify=False, headers=self._headers, params=filters, timeout=self.timeout,
        ) as response:
            response.raise_for_status()
            return response.json()['data']

    def list_cluster_role_bindings(self) -> List[ClusterRoleBinding]:

        url = f"{self.url}/v3/clusterRoleTemplateBindings"

        with requests.get(
            url, verify=False, headers=self._headers, timeout=self.timeout,
        ) as response:
            response.raise_for_status()
            return response.json()['data']





