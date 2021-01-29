from typing import List
import attr

from app.rancher import RancherService
from app.entities import Cluster, ClusterRoleBinding, ClusterMember
from app.steps import list_clusters, list_cluster_members, aggregate_cluster_members, generate_rbac_csv, \
    save_rbac, remove_local_members as rm_local_members


@attr.s(auto_attribs=True)
class PipelineState:
    rbac_csv: str = None
    clusters: List[Cluster] = attr.ib(default=[])
    bindings: List[ClusterRoleBinding] = attr.ib(default=[])
    members: List[ClusterMember] = attr.ib(default=[])


@attr.s(auto_attribs=True)
class Pipeline:
    rancher_service: RancherService

    def __attrs_post_init__(self):
        self._state = PipelineState()

    def list_all_clusters(self):
        self._state.clusters = list_clusters(self.rancher_service)
        return self

    def list_all_members(self):
        self._state.bindings = list_cluster_members(self.rancher_service)
        return self

    def remove_local_members(self):
        self._state.bindings = rm_local_members(self._state.bindings)
        return self

    def aggregate_cluster_members(self):
        self._state.members = aggregate_cluster_members(self._state.clusters, self._state.bindings)
        return self

    def generate_rbac_csv(self):
        self._state.rbac_csv = generate_rbac_csv(self._state.members)
        return self

    def save_configmap(self):
        save_rbac(self._state.rbac_csv)
